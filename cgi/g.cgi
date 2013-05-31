#!/usr/bin/perl

BEGIN { require '.poem'; }

use strict;
use utf8;
use lib $ENV{POEM_LIB_ROOT};

use POEM::HTTP::Request;
use POEM::HTTP::Response;

use POEM::Session;
use POEM::Auth;

use POEM::Entity;
use POEM::Container;
use POEM::DBC;
use POEM::DB::Filter;
use POEM::HTTP::Util;

use POEM::Conf;

use POEM::Template;

use Time::HiRes qw(gettimeofday tv_interval);

use vars qw/$Request $Session $Cookies $Response $INPUT $GConf %template_vars/;
use vars qw/$Images $Image $Total $West $South $registered/;

$Request  = POEM::HTTP::Request->new();
$Request->filter();
$INPUT    = $Request->getInput;
$GConf    = POEM::Conf->new("gallery");

# check and load session data
$Session = POEM::Session->new();
$Cookies = $Request->getCookies;
$Cookies->{sess} and $Session->load($Cookies->{sess});
$Session->ID or $Session->newID();

# проверяем пользователя с таким ID
if ( defined $Session->{user} )
{
    if ( my $user = POEM::Auth->getUser($Session->{user}) )
    {
        $ENV{POEM_USER} = $user;
    }
    else
    {
        # удаляем его ID из сессии
        delete $Session->{user};
    }
}

$Response = POEM::HTTP::Response->new();
$Response->setCookie( { name => 'sess' , value => $Session->ID, expires => time + $Session->getExpire, path => '/', domain => '.'.$ENV{HTTP_HOST} } );

# store session on persistent storage
$Session->save();

$ENV{POEM_USER}{SESSION} = $Session;

$ENV{PATH_INFO} =~ s/\/$//;
my $path = $ENV{DOCUMENT_ROOT} . $ENV{PATH_INFO};

if (-d $path)
{
  $INPUT->{mode} ||= 'list';
}
if (-f $path)
{
  $INPUT->{mode} ||= 'screen';
}

$INPUT->{mode} ||= 'favorites';

$registered = $ENV{POEM_USER}->ID ? 1 : 0;

if ($INPUT->{mode} eq 'map')
{
  $INPUT->{'-filt.labels'} = '3';
  my ($s,$w) = split(',',$INPUT->{sw});
  my ($n,$e) = split(',',$INPUT->{ne});
  $INPUT->{'-filt.norther'} = $South = $s;
  $INPUT->{'-filt.souther'} = $n;
  $INPUT->{'-filt.wester'} = $e;
  $INPUT->{'-filt.easter'} = $West = $w;
}

if ($INPUT->{layout} eq 'rss')
{
  $INPUT->{'-nav.sort'} = 'ctime DESC';
}

# множественное сохранение
if ($INPUT->{images})
{
  foreach my $img (@{$INPUT->{images}})
  {
    my $image = POEM::Entity->new('gallery::image')->load($img->{id});
    $image->set($img)->save()->setLabels($img->{labels});
    if ($img->{shrink})
    {
      shrink($image);
    }
  }
  my $qs = '?'.join(';', map { $_.'='.POEM::HTTP::Util::URLencode($INPUT->{$_}) } grep { /^(:?\mode|\-nav\.|\-filt\.)/ } keys(%{$INPUT}));
  $Response->redirect($qs);
}

# единичное сохранение
if ($INPUT->{id})
{
  my $image = POEM::Entity->new('gallery::image')->load($INPUT->{id});
  $image->set($INPUT)->save()->setLabels($INPUT->{labels});
  if ($INPUT->{shrink})
  {
    shrink($image);
  }
  my $qs = '?'.join(';', map { $_.'='.POEM::HTTP::Util::URLencode($INPUT->{$_}) } grep { /^(:?\mode|\-nav\.)/ } keys(%{$INPUT}));
  $Response->redirect($qs);
}

my %ACTIONS = (
    'adminlist'  => \&list,
    'list'       => \&list,
    'jsonlist'   => \&list,
    'map'        => \&maplist,
    'favorites'  => \&favorites,
    'edit'       => \&info,
    'info'       => \&info,
    'json'       => \&info,
    'jsonget'    => \&get,
    'infobox'    => \&get,
    'screen'     => \&screen,
    'export'     => \&export,
    'original'   => \&original,
    'remove'     => \&remove,
    'rotate'     => \&rotate,
    'thumbnail'  => \&thumbnail,
    'rating'     => \&rating,
    'log'        => \&log,
    'favoritize' => \&favoritize
);

# обрабатываем действия
map { doAction($_) } ( split(/,/o,$INPUT->{mode}) ) if (defined $INPUT->{mode});

# HACK!
if ($INPUT->{mode} eq 'list' && $INPUT->{layout} && $INPUT->{mode} ne $INPUT->{layout})
{
  $INPUT->{mode} = $INPUT->{layout};
}

my $template = POEM::Template->new($GConf->{templates}{$INPUT->{mode}});
die "Can't open template $template: ".$template->getErrorMessage."\n" if $template->getError;
$template->do(getTemplateVars());
$Response->out($template->getOutput);
$Response->flush();

# === ACTIONS ===

sub doAction
{
  while (my $action = shift)
  {
    &{$ACTIONS{$action}} if defined $ACTIONS{$action};
  }
}

sub favorites
{
  $INPUT->{'-filt.user'} = $ENV{POEM_USER}->ID == 1 ? $INPUT->{'-filt.user'} || $ENV{POEM_USER}->ID : $ENV{POEM_USER}->ID;
  list();
}

sub list
{
  my $enum = $INPUT->{mode} eq 'jsonlist';
  my $ic = POEM::Container->new('gallery::image');
  if ($ENV{PATH_INFO})
  {
    my $bundle = $ENV{PATH_INFO};
    $bundle =~ s/$GConf->{galleries}{root}//;
    $ic->fixupBundle($bundle);
    $INPUT->{'-filt.bundle'} = $bundle;
  }
  $INPUT->{'-nav.distinct'} = 1;
  $INPUT->{'-nav.sort'} ||= 'stime ASC';
  $INPUT->{'-filt.censored'} = $ENV{POEM_USER}->{censorship} || 0;
  if ($INPUT->{layout} eq 'map')
  {
    $INPUT->{'-filt.located'} = 1;
    $INPUT->{'-nav.sort'} = 'lng ASC, lat ASC, prefered DESC';
  }
  my $qd = POEM::DB::Filter->new($ic->getConfig())->makeQueryDescriptor($INPUT);
  my @having = ();
  if ($INPUT->{'-filt.labels'})
  {
    push(@having, map('SUM(IF(label='.$_.',1,0)) > 0', split(/,\s*/, $INPUT->{'-filt.labels'})));
    $qd->{'group'} = 'image';
  }
  if ($INPUT->{'-filt.notlabels'})
  {
    push(@having, map('SUM(IF(label='.$_.',1,0)) = 0', split(/,\s*/, $INPUT->{'-filt.notlabels'})));
    $qd->{'group'} = 'image';
  }
  $qd->{'having'} = join(' AND ', @having);
  $Total = $ic->count($qd);

  $qd->{'from'} = 0 + $INPUT->{'-nav.start'};
  $qd->{'num'} = $INPUT->{'-nav.limit'} ? $INPUT->{'-nav.limit'} :
                 $INPUT->{mode} eq 'jsonlist' || $INPUT->{layout} eq 'map' || $INPUT->{mode} eq 'map' ? 10000 : 
                 $INPUT->{mode} eq 'adminlist' ? 100 : 
                 $INPUT->{layout} eq 'rss' ? 20 : 
                 10;
  $Images = $enum ? $ic->getRecords('id, bundle, name, description', $qd) : $ic->list($qd);

  if ($INPUT->{shrinkall} && POEM::Auth->isUserInRole($ENV{POEM_USER}, 'administrator'))
  {
    print STDERR "forking\n";
    $qd->{'from'} = 0;
    $qd->{'num'} = 10000;
    my $images = $ic->list($qd);
    # операция длинная, поэтому форкаемся
    fork() && return;
    $ENV{PATH} = '/bin:/usr/bin';
    close STDOUT; close STDERR; close STDIN;
    chdir '/';
    require 'sys/syscall.ph';
    syscall(&SYS_setsid);
    $SIG{'INT'} = $SIG{'QUIT'} = $SIG{'TERM'} = 'exit';
    $SIG{'HUP'} = 'ignore';

    open(*STDERR,'>/tmp/log.log');
    select(STDERR);
    print STDERR "forked\n";
    
    foreach my $image (@{$images})
    {
      shrink($image);
    }
    
    close(STDERR);
    exit;
  }
}

sub get
{
  $Image = POEM::Entity->new('gallery::image')->load($INPUT->{'-filt.id'}, 1);
  unless ($Image->ID)
  {
    $Response->setStatus(404);
    $Response->flush();
    exit;
  }
}

sub info
{
  $Image = POEM::Entity->new('gallery::image')->loadByPath($ENV{PATH_INFO});
  unless ($Image->ID)
  {
    $Response->setStatus(404);
    $Response->flush();
    exit;
  }
}

sub export
{
  $Image = POEM::Entity->new('gallery::image')->loadByPath($ENV{PATH_INFO},0);
  unless ($Image->{exportable})
  {
    $Response->setStatus(403);
    $Response->noCache();
    $Response->flush();
    exit;
  }
  screen(1);
}

sub screen
{
  my $export = shift || 0;
  my $slideshow = $INPUT->{format} eq 'slideshow';
  my $file_lastmod = (stat($path))[9];
  $Response->setHeader('Last-Modified', POSIX::strftime('%a, %d %b %Y %T GMT', gmtime($file_lastmod)));
  my $etag = $path;
  $etag =~ s|\Q$ENV{DOCUMENT_ROOT}\E/?||;
  $etag =~ s|[/.]|_|g;
  $Response->setHeader('Etag', $etag);
  if ($ENV{HTTP_IF_MODIFIED_SINCE})
  {
    require Time::ParseDate;
    my $since = Time::ParseDate::parsedate($ENV{HTTP_IF_MODIFIED_SINCE});
    if ($since >= $file_lastmod)
    {
      $Response->notModified();
      exit;
    }
  }

  if (! $registered && ! $export)
  {
    $path = $ENV{DOCUMENT_ROOT} . '/site/img/image_lock.png';
    $Response->setStatus(403);
    $Response->noCache();
  }
  else
  {
    # Expires - один месяц для примера
    $Response->setHeader('Expires',POSIX::strftime('%a, %d %b %Y %T GMT', gmtime(time()+30*24*60*60)));
  }
  require Image::Magick;
  my $image = Image::Magick->new();
  $image->Read($path);
  (my $ox, my $oy) = $image->Get('width','height');
  my $rx = $export ? $GConf->{sizes}{export_max_width} || 400 : $GConf->{sizes}{screen_max_width} || 800;
  my $ry = $export ? $GConf->{sizes}{export_max_height} || 300 : $GConf->{sizes}{screen_max_height} || 600;
  my $nx;
  my $ny;
  if ($slideshow)
  {
    $ny = $GConf->{sizes}{slideshow} || 480;
    $nx = int($ox / $oy * $ny);
  }
  elsif ($ox > $oy)
  {
    $nx = $rx;
    $ny = int($oy / $ox * $nx);
  }
  else
  {
    $ny = $ry;
    $nx = int($ox / $oy * $ny);
  }
  my $pct = (100 + $GConf->{sizes}{screen_delta}) / 100;
  if ($ox > int($nx * $pct) || $oy > int($ny * $pct))
  {
#    my $t0 = [gettimeofday];
    my $e = $image->Resize(width=>$nx, height=>$ny);
#    my $t1 = [gettimeofday];
#    my $elapsed = tv_interval($t0, $t1);
#    print STDERR "Resize: $elapsed s\n";
    if ($e)
    {
      print STDERR "Screen image creation error: $e\n";
      return undef;
    }
  }
  require File::MMagic;
  my $mm = new File::MMagic;

  my $blob = ($image->ImageToBlob())[0];
  $Response->setContentType($mm->checktype_contents($blob));
#  $Response->setHeader('Content-Length', -s ???
  $Response->setAutoFlush();
  $Response->out($blob);
  $Response->flush();
  
  if ($registered && ! $slideshow)
  {
    $Image = POEM::Entity->new('gallery::image')->loadByPath($ENV{PATH_INFO},0);
    POEM::DBC->new()->do("INSERT INTO gallery_image_log VALUES(".$Image->ID.",".$ENV{POEM_USER}->ID.",".($export ? 3 : 1).",NOW())") if ($ENV{POEM_USER}->ID);
  }

  exit;
}

sub rotate
{
  require Image::Magick;
  my $image = Image::Magick->new();
  my $path = $ENV{DOCUMENT_ROOT}.$ENV{PATH_INFO};
  $image->Read($path);
  $image->Rotate(degrees => $INPUT->{degrees});
  $image->Write($path);
  remove_thumbnail($path);
  $Response->redirect($ENV{HTTP_REFERER});
}

sub remove
{
  POEM::Entity->new('gallery::image')->loadByPath($ENV{PATH_INFO},0)->remove();
  $Response->redirect($ENV{HTTP_REFERER});
}

sub shrink
{
  my $img = shift;
  require Image::Magick;
  my $image = Image::Magick->new();
print STDERR ">>>$img->{path}\n";
  $image->Read($ENV{DOCUMENT_ROOT}.$img->{path});
  (my $ox, my $oy) = $image->Get('width','height');
print STDERR ">>>$ox,$oy\n";
  my $nx;
  my $ny;
  if ($ox > $oy)
  {        
    $nx = $GConf->{sizes}{screen_max_width} || 800;
    $ny = int($oy / $ox * $nx);
  }
  else
  {
    $ny = $GConf->{sizes}{screen_max_height} || 600;
    $nx = int($ox / $oy * $ny);
  }
  my $pct = (100 + $GConf->{sizes}{screen_delta}) / 100;
  if ($ox > int($nx * $pct) || $oy > int($ny * $pct))
  {
    my $t0 = [gettimeofday];
    my $e = $image->Resize(width=>$nx, height=>$ny);
    if ($e)
    {
      print STDERR "Shrink image creation error: $e\n";
      return undef;
    }
    $image->Write($ENV{DOCUMENT_ROOT}.$img->{path});
  }
}

sub original
{
  my $filename = ($path =~ /\/([^\/]+)$/)[0];

  $Image = POEM::Entity->new('gallery::image')->loadByPath($ENV{PATH_INFO},0);
  unless ($Image->ID)
  {
    $Response->setStatus(404);
    $Response->flush();
    exit;
  }
  $Response->setHeader("Content-Disposition","attachment; filename=$filename");
  $Response->setContentType(qq(application/x-force-download; name="$filename"));

  unless ($registered)
  {
    $path = $ENV{DOCUMENT_ROOT} . '/site/img/image_lock.png';
    $Response->setStatus(403);
    $Response->noCache();
  }

  my $size = -s $path;
  $Response->setHeader('Content-Length', $size);
  $Response->setAutoFlush();
  open(FILE, $path);
  binmode(FILE);
  {
    local $/;
    $Response->out(<FILE>);
  }
  close(FILE);
  $Response->flush();
  if ($registered)
  {
    POEM::DBC->new()->do("INSERT INTO gallery_image_log VALUES(".$Image->ID.",".$ENV{POEM_USER}->ID.",0,NOW())");
  }
  exit;
}

sub maplist
{
  list();

  $Response->setContentType("text/xml");
  $Response->setAutoFlush();

  my $out = <<END;
<?xml version="1.0" encoding="Windows-1251"?>
<items>
END
#    <cluster count="19" id="3eabf8">
#        <center lat="64.923541743065" lng="36.9140625" />
#        <avg lat="65.0334280781123" lng="35.754422933136" />
#        <bounds s="64.168106897992" n="65.658274519827" w="35.15625" e="38.671875" />
#        <span width="0.733680725097976" height="0.236047293017279" />
#    </cluster>

    my $clusters = {};

    my $ppd = $INPUT->{ppd}; # pixels per degree
    my $dd = 20 / $ppd;
    my $cim;
    my $lng = $West;
    my $lat = $South;

#    my @images = sort bydistance @{$Images};



#    foreach my $image (@{$Images})
#    {
#       if (! $cim || $cim->{lng} > $image->{lng})
#       {
#         $cim = $image;
#         next;
#       }

#       $cim = $image;
#    }



    foreach my $image (@{$Images})
    {
      $out .= <<END;
    <image id="$image->{id}">
        <center lat="$image->{lat}" lng="$image->{lng}" />
        <span width="0.062227249145508" height="0.031560175648202" />
        <title>$image->{name}</title>
        <author>Olya</author>
        <preview src="/thumbx/ee6/2093476.jpg" width="120" height="150" />
    </image>
END
    }
  $out .= <<END;
</items>
END
  $Response->out($out);
  $Response->flush();
  exit;
}

sub acos { atan2( sqrt(1 - $_[0] * $_[0]), $_[0] ) }

sub distance
{
  my $lat1 = $_[0]->{lat} / 57.29577951;
  my $lng1 = $_[0]->{lng} / 57.29577951;
  my $lat2 = $_[1]->{lat} / 57.29577951;
  my $lng2 = $_[1]->{lng} / 57.29577951;

  return 0 if ($lng1 == $lng2 && $lat1 == $lat2);
  return acos(sin($lat1)*sin($lat2)+cos($lat1)*cos($lat2)*cos($lng2-$lng1))*6371; # kilometres
}

sub remove_thumbnail
{
  my $path = shift;

  my $tpath = $path;
  $tpath =~ s/\/([^\/]+)$//;
  my $file = $1;
  my $tdir = $tpath . '/thumbs';
  $tpath .= '/thumbs/t-'.$file;
  if (-f $tpath)
  {
    unlink $tpath;
  }
  return $tpath;
}

sub thumbnail
{
  my $path = $ENV{DOCUMENT_ROOT} . $ENV{PATH_INFO};
  my $tpath = $path;
  $tpath =~ s/\/([^\/]+)$//;
  my $file = $1;
  my $tdir = $tpath . '/thumbs';
  $tpath .= '/thumbs/t-'.$file;

  POEM::DBC->new()->disconnect();

  if ($registered && ! fork())
  {
    my $t2 = [gettimeofday];
    $Image = POEM::Entity->new('gallery::image')->loadByPath($ENV{PATH_INFO},0);
    POEM::DBC->new()->do("INSERT INTO gallery_image_log VALUES(".$Image->ID.", ".$ENV{POEM_USER}->ID.", 4, NOW())");
    my $t3 = [gettimeofday];
    print STDERR "DB: ".tv_interval($t2, $t3)." s\n";
    exit(0);
  }

  require File::MMagic;
  my $mm = new File::MMagic;

  $Response->setContentType($mm->checktype_filename($tpath));
  my $size = -s $tpath;
  my $lastmod = (stat(_))[9];
  $Response->setHeader('Content-Length', $size);
  if ($registered)
  {
    require POSIX;
    $Response->setHeader('Last-Modified', POSIX::strftime('%a, %d %b %Y %T GMT', gmtime($lastmod)));
    my $etag = $tpath;
    $etag =~ s/$ENV{DOCUMENT_ROOT}\///;
    $etag =~ s/[\/\.]/_/g;
    $Response->setHeader('Etag',chr(34).$etag.chr(34));
    $Response->setHeader('Expires', POSIX::strftime('%a, %d %b %Y %T GMT', gmtime(time()+2592000))); #one month
  }
  else
  {
    $Response->noCache();
  }

#HTTP_IF_NONE_MATCH=>"galleries_places_Petersburg_thumbs_t-IMG_0579_JPG"
#HTTP_IF_MODIFIED_SINCE=>Fri, 14 Jan 2005 15:46:46 GMT
  if ($ENV{HTTP_IF_MODIFIED_SINCE})
  {
    require Time::ParseDate;
    my $since = Time::ParseDate::parsedate($ENV{HTTP_IF_MODIFIED_SINCE});
    if ($since >= $lastmod)
    {
      $Response->notModified();
    }
  }

  $Response->setAutoFlush();
  open(FILE, $tpath);
  binmode(FILE);
  {
    local $/;
    $Response->out(<FILE>);
  }
  close(FILE);
  $Response->flush();
  exit;
}

sub log
{
  if ($ENV{POEM_USER} && $ENV{POEM_USER}->ID)
  {
    POEM::DBC->new()->do("INSERT INTO gallery_image_log VALUES(".$INPUT->{identity}.", ".$ENV{POEM_USER}->ID.", ".$INPUT->{status}.", NOW())");
  }
  $Response->setStatus(204);
  $Response->flush();
  exit;
}

sub rating
{
# average=2.199072356215214&identity=8215&max=5&rated=4&rerated=true&total=539&mode=rating
  POEM::DBC->new()->do("REPLACE INTO gallery_image_rating VALUES(".$INPUT->{identity}.",".$ENV{POEM_USER}->ID.",".$INPUT->{rated}.")");

  $Response->setStatus(204);
  $Response->flush();
  exit;
}

sub favoritize
{
  if ($ENV{POEM_USER} && $ENV{POEM_USER}->ID)
  {
    require Publish::Gallery::Favorites;
    my $favorites = Publish::Gallery::Favorites->new($ENV{POEM_USER});
    $favorites->favoritize($INPUT->{identity}, $INPUT->{favoritize});
  }
  $Response->setStatus(204);
  $Response->flush();
  exit;
}


sub getTemplateVars()
{
  unless (keys %template_vars)
  {
    $template_vars{ENV}           = \%ENV;
    $template_vars{Request}       = $Request;
    $template_vars{Response}      = $Response;
    $template_vars{Session}       = $Session;
    $template_vars{Input}         = $INPUT;
    $template_vars{User}          = $ENV{POEM_USER};
    $template_vars{Images}        = $Images;
    $template_vars{Total}         = $Total;
    $template_vars{Image}         = $Image;
    $template_vars{mode}          = $INPUT->{mode};
    $template_vars{Configuration} = $GConf;
    $template_vars{Registered}    = $registered;
  }
  return \%template_vars;
}
