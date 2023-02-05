#!/usr/bin/perl
use warnings;
use strict;
use v5.20;
use utf8;
no warnings "experimental::signatures";
use feature qw(postderef signatures);

use File::Basename;
use lib dirname (__FILE__);

package ActionType;

our @action_type_field_names = qw(
    action_type_id
    negative_form
    interrogative_form
    subject
    verb
    object
    auxiliary_verb
    modus
    tense
    passive_form
    pre_vp
    post_vp
    object_case
    score
    global_score
    source
    text
);

our @false_keys = qw(negative_form interrogative_form passive_form);

# Initialize blank action type.
sub action_type() { return {map { $_ => default_value($_) } @action_type_field_names}; }

sub default_value($key) { return grep(/$key/, @false_keys) ? "FALSE" : "NONE"; }

sub is_set($action_type, @keys) { return !grep { "$action_type->{$_}" eq default_value($_) } @keys; }

# Concatenate values with delimiter ';'.
sub add_value($action_type, $key, $value) {
    my $curr_value = $action_type->{$key};
    $action_type->{$key} = ("$curr_value" eq default_value($key) ? $value : "$curr_value;$value");
}

1;
