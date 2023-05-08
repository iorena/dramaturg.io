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

# Keys which are fields in the output.
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
    object_case
    object_number
    pre_vp
    post_vp
    score
    global_score
    source
    text
);

# Keys whose default values should be "FALSE" instead of "NONE".
our @false_keys = qw(
    negative_form
    interrogative_form
    passive_form
    has_other
);

# Private keys which will not be output but which contain important information necessary for correct program logic.
our @private_keys = qw(
    subject_is_propn
    object_is_propn
    subject_id
    object_id
    has_other
);

our $separator = ';';

# Initialize blank action type.
sub action_type() { return {map { $_ => default_value($_) } (@action_type_field_names, @private_keys)}; }

sub default_value($key) { return grep(/$key/, @false_keys) ? "FALSE" : "NONE"; }

sub is_set($action_type, @keys) { return !grep { "$action_type->{$_}" eq default_value($_) } @keys; }

# Concatenate values with delimiter ';'.
sub add_value($action_type, $key, $value) {
    my $curr_value = $action_type->{$key};
    $action_type->{$key} = ("$curr_value" eq default_value($key) ? $value : $curr_value . $separator . $value);
}

# Get concatenated non-default value(s) as a list.
sub get_values($action_type, $key) { return grep { $_ ne default_value($key) } split($separator, $action_type->{$key}); }

1;
