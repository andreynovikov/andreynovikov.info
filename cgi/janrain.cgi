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
$Response->setCookie( { name => 'sess' , value => $Session->ID, expires => time + $Session->getExpire, path => '/' } );

# Step 1) Extract the token from your environment. If you are using app engine,

my $token = $INPUT->{token};

# Step 2) Now that we have the token, we need to make the api call to auth_info.
# auth_info expects an HTTP Post with the following paramters:
my @api_params = [
    'token' => $token,
    'apiKey'=> '88ee928b0b69288820a89d47e7c2250e59d80bcb',
    'format'=> 'json'
];

# make the api call
my $userAgent = LWP::UserAgent->new();
my $response = $userAgent->post('https://rpxnow.com/api/v2/auth_info', @api_params);
die "Error: ", $response->status_line unless ($response->is_success);

# read the json response
my $auth_info_json = $response->content;
print STDERR $auth_info_json;

# Step 3) process the json response
my $json = JSON->new->allow_nonref;
my $auth_info = $json->decode($auth_info_json);
print STDERR $json->pretty->encode($auth_info); # pretty-printing

# Step 4) use the response to sign the user in
if ($auth_info->{stat} eq 'ok')
{
  my $profile = $auth_info->{profile};
  # 'identifier' will always be in the payload
  # this is the unique idenfifier that you use to sign the user in to your site
  my $identifier = $profile->{identifier};

  my $User;
  my $users = POEM::Container->new('poem::user');
  my $u = $users->list( { where => "login=".$users->getDBC->quote($identifier) } );
  if (@$u)
  {
    $User = $u->[0];
  }
  else
  {
    # сохраняем введенные данные
#    profile_pic_url = profile.get('photo')
    my $newUser = POEM::Entity->new('poem::user');
    $newUser->set({
                    login => $profile->{identifier},
                    provider => $profile->{providerName},
                    name => $profile->{displayName},
#                    censorship => 1,
                    email => $profile->{email}
                  })->save();
    if ($newUser->getError())
    {
      $Response->redirect('/user/login.xhtml?errmsg='.POEM::HTTP::Util::URLencode('системная ошибка, обратитесь к администратору сервера'));
    }

#    $newUser->set({roles => $newUser->{roles} | 16})->save();
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
    $Response->redirect('/');
  }
}
else
{ 
  $Response->redirect('/user/login.xhtml?errmsg='.POEM::HTTP::Util::URLencode($auth_info->{err}->{msg}));
}
