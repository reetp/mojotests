#!/usr/bin/perl

use strict;
use warnings;
use utf8;

use Mojolicious::Lite;
use esmith::DB;
use esmith::ConfigDB;

# Mojolicious::Lite
plugin 'TagHelpers';

my $configDB = esmith::ConfigDB->open_ro or die("can't open Config DB test");

my $key = 'sshd';
my $myKeyStatus = $configDB->get_prop( $key, 'status' ) || 'disabled';

my $data = "";
$data .= "A new line<br>";
$data .= "Some Text<br/>";
$data .= "some more Text<br/>";

my $networksDB = esmith::ConfigDB->open('networks') or die("Error - cant connect to networks database");

get '/' => sub {

    my ($mojo) = @_;

    # my $c = shift;

    # my $test = $c->param('Key Value:');
    # my $text        = "Key $key is";

    my @connections = $networksDB->keys;

    foreach my $network (@connections) {

        my $netmask = $networksDB->get_prop( $network, 'Mask' ) || "";

        #$c->stash (network => $network);
        # This will ONLY stash the last value and not an array.
        $mojo->stash( network => $network, netmask => $netmask );

        # This produces an array something like this:
        # ('fish', 'carrot', 'egg', 'spoon', 'banana')
        my @stuff = qw ( fish carrot egg spoon banana );

        # Still not sure how to do this
        # To select a default value we have to get an array more like this (just demo stuff)
        # [[Germany => 'de', selected => 'selected'], [English => 'en'], 'us']
        # This should give us something like
        # <option selected="selected" value="de">Germany</option>
        # Either need to setup the array differently, or modify the select_field template line
        # Probably the latter

        $mojo->stash( 'stuff' => \@stuff );

    }

    #$c->render(text => "$text $myKeyStatus</br>New Line<br />$data");
    #$c->render(template=>'hello');
    # $mojo->render( template => 'hello', foo => 'test', bar => 23 );
    $mojo->render( template => 'hello' );
};

# This answers http 'GET'
get '/update' => sub {
    print 'hello';
};

# This answers http 'POST'

# Access request information
# This will output the browser data - the form user /agent to get here
# no idea yet how to get the posted form data

post '/agent' => sub {

    my $c    = shift;
    my $host = $c->req->url->to_abs->host;
    my $ua   = $c->req->headers->user_agent;
    my $data = $c->param('networks');
    my $pass = $c->param('pass');
    my $radio= $c->param('country');
    $c->render( text => "Request by $ua reached $host. <br />Form data is $data <br /> Country is $radio <br />Pass is $pass");

};

app->start;

__DATA__
@@hello.html.ep

%= stylesheet 'http://10.0.0.158/perltest/foo.css'
%= stylesheet begin
  body {color: #f70000}
% end

Hello Template Text
<br />

<br />

 % my $networksDB = esmith::ConfigDB->open('networks') or die("Error - cant connect to networks database");

    % my @connections = $networksDB->keys;
    <table><tbody>
    <tr>
    <td>Network</td><td>Netmask</td>
    </tr>
    
    % foreach my $network (@connections) {

    <tr>
      % my $netmask = $networksDB->get_prop( $network, 'Mask' ) || "";
        <td><%= $network %><br /></td>
        <td><%= $netmask %><br /></td>
      % }
    </tr>
    </tbody></table>

<form name="networks" action="./readtest1.cgi/agent" method="POST">


<div>
<%= select_field 'networks' => [ @{ stash('stuff') }], id=> 'dropdown' %>
</div>

<div>
% param country => 'germany' unless param 'country';

<%= radio_button 'country' => 'germany' %> Germany
<%= radio_button 'country' => 'france'  %> France
<%= radio_button 'country' => 'uk'      %> UK
</div>

<div>
Password
<%= password_field 'pass', id => 'foo' %>
<br />
</div>
<input type="submit" value="Submit">

</form>

<br /><br />
