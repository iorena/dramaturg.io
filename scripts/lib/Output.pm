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

package Output;

sub print_action_type_headers() { say join("\t", @ActionType::action_type_field_names); }
sub print_action_type($action_type) { say join("\t", map { $action_type->{$_} } @ActionType::action_type_field_names); }
sub print_action_types(@action_types) { print_action_type($_) for @action_types; }

sub print_project_word($project_words) { say join(",", map { $project_words->{$_} } qw(score subject verb object object_case)); }
sub print_project_words(@project_words) { print_project_word($_) for @project_words; }

1;
