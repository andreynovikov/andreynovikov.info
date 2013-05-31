#!/usr/bin/perl

BEGIN { require '.poem'; }

use strict;
use lib $ENV{POEM_LIB_ROOT};

use JSON;
use LWP::UserAgent;
use HTTP::Request::Common;

use POEM::HTTP::Request;
use POEM::HTTP::Response;

use POEM::Session;
use POEM::Auth;

use POEM::Entity;
use POEM::Container;

use vars qw/$Request $Session $Cookies $Response $INPUT/;

$Request  = POEM::HTTP::Request->new();
$Request->filter();
$INPUT    = $Request->getInput;

$Session = POEM::Session->new();
#$Cookies = $Request->getCookies;
#$Cookies->{sess} and $Session->load($Cookies->{sess});
$Session->ID or $Session->newID();

$Response = POEM::HTTP::Response->new();
$Response->setCookie( { name => 'sess' , value => $Session->ID, expires => time + $Session->getExpire, path => '/', domain => '.'.$ENV{HTTP_HOST} } );

my $token = $INPUT->{'connection_token'};

my $site_subdomain = 'novikov';
my $site_public_key = 'f04a5e14-708f-479a-8ebd-0465dd48db30';
my $site_private_key = '48da05fb-9318-4626-a296-d7b95ee2e42a';

my $site_domain = $site_subdomain.'.api.oneall.com';
my $resource_uri = 'https://'.$site_domain.'/connections/'.$token .'.json';

# Get token

my $userAgent = LWP::UserAgent->new();
my $request = HTTP::Request->new(GET => $resource_uri);
$request->authorization_basic($site_public_key, $site_private_key);
my $response = $userAgent->request($request);
die "Error: ", $response->status_line unless ($response->is_success);

# Get auth info

my $content = $response->content;
my $json = JSON->new->allow_nonref;
my $data = $json->decode($content);

print STDERR $json->pretty->encode($data); # pretty-printing

if ($data->{response}->{result}->{status}->{code} != 200 || $data->{response}->{result}->{data}->{plugin}->{key} ne 'social_login')
{
  $Response->redirect('/user/login.xhtml?errmsg='.POEM::HTTP::Util::URLencode($data->{response}->{result}->{status}->{info}));
  exit(0);
}

my $auth_info = $data->{response}->{result}->{data};
my $profile = $auth_info->{user}->{identity};
my $identifier = $auth_info->{user}->{user_token};

my $User;
my $users = POEM::Container->new('poem::user');
my $u = $users->list( { where => "login=".$users->getDBC->quote($identifier) } );
if (@$u)
{
  $User = $u->[0];
}
else
{
  my $newUser = POEM::Entity->new('poem::user');

  my $userUrl;
  if ($profile->{urls})
  {
    foreach my $url (@{$profile->{urls}})
    {
      if ($url->{type} eq 'profile')
      {
        $userUrl = $url->{value};
        last;
      }
    }
  }

  my $userEmail;
  if ($profile->{emails})
  {
    $userEmail = $profile->{emails}->[0]->{value};
  }

  $newUser->set({
                  login => $identifier,
                  provider => $profile->{provider},
                  name => $profile->{displayName},
#                  censorship => $profile->{provider} eq 'vkontakte' ? 1 : 0,
                  url => $userUrl,
                  email => $userEmail
                })->save();
  if ($newUser->getError())
  {
    $Response->redirect('/user/login.xhtml?errmsg='.POEM::HTTP::Util::URLencode('системная ошибка, обратитесь к администратору сервера'));
  }

#  $newUser->set({roles => $newUser->{roles} | 16})->save();
  $User = $newUser;
}

$Session->set({ user => $User->ID });
$Session->save();

my $back = $Request->getValues('-back')->[0] || $INPUT->{'-back'};
if ($back && $back ne '' && $back ne ',')
{
  $Response->redirect($back);
}
else
{
  $Response->redirect('/galleries/');
}

