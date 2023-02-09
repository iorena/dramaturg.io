#!/usr/bin/perl
use warnings;
use strict;
use v5.20;
use utf8;
no warnings "experimental::signatures";
use feature qw(postderef signatures);

use File::Basename;
use lib dirname (__FILE__);

use ActionType;
use Output;
use Utils;

package ActionTypePostProcessor;

our @sort_keys = qw(
    negative_form
    interrogative_form
    subject
    verb
    object
    auxiliary_verb
    modus
    tense
    passive_form
    has_vp
    object_case
    object_number
);

sub custom_sort($a, $b) {
    for(@sort_keys) {
        my $sort_val = $a->{$_} cmp $b->{$_};
        return $sort_val if $sort_val != 0;
    }
    return 0;
}

sub combine_action_types(@action_types) {
    my $action_type = ActionType::action_type();
    $action_type->{$_} = $action_types[0]->{$_} for @sort_keys;

    if (ActionType::is_set($action_type, "has_vp")) {
        $action_type->{'pre_vp'} = ActionType::add_value($action_type, 'pre_vp', $_) for (sort keys {map { $_ => 1 } map { ActionType::get_values($_, 'pre_vp') } @action_types}->%*);
        $action_type->{'post_vp'} = ActionType::add_value($action_type, 'post_vp', $_) for (sort keys {map { $_ => 1 } map { ActionType::get_values($_, 'post_vp') } @action_types}->%*);
    }

    $action_type->{'score'} = Utils::average(map { $_->{'score'} } @action_types);
    $action_type->{'global_score'} = Utils::average(map { $_->{'global_score'} } @action_types);
    ActionType::add_value($action_type, 'source', $_->{'action_type_id'}) for @action_types;

    return $action_type;
}

sub post_process_action_types(@documents) {
    my @sorted_action_types = sort { custom_sort($a, $b) } map { $_->{'action_types'}->@* } @documents;
    Output::log_msg("Post-processing " . scalar(@sorted_action_types) . " action types.\n");

    my @action_types;

    my ($i, $n_combined_action_types) = (0) x 2;

    while ($i <= $#sorted_action_types) {
        my $action_type = $sorted_action_types[$i];

        # Find range ($i, ..., $j) of combinable action types.
        my $j = $i;
        ++$j while $j + 1 <= $#sorted_action_types && custom_sort($action_type, $sorted_action_types[$j + 1]) == 0;

        if ($i != $j) {
            my $combined_action_type = combine_action_types(@sorted_action_types[$i..$j]);
            $combined_action_type->{'action_type_id'} = sprintf("ATC%04d", ++$n_combined_action_types);
            Output::log_msg("New combined action type:");
            Output::log_action_type($combined_action_type);
            push @action_types, $combined_action_type;
        } else {
            push @action_types, $action_type;
        }

        $i = $j + 1;
    }

    return @action_types;
}

1;
