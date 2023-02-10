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

our $execname = "";
our $logfile = "";
our $action_type_output_separator = '\t';
our $project_words_output_separator = '\t';

sub print_action_type_headers() { say join($action_type_output_separator, @ActionType::action_type_field_names); }
sub print_action_type($action_type) { say join($action_type_output_separator, map { $action_type->{$_} } @ActionType::action_type_field_names); }
sub print_action_types(@action_types) { print_action_type($_) for @action_types; }

sub print_project_word($project_words) { say join($project_words_output_separator, map { $project_words->{$_} } ('score', 'subject', 'verb', 'object', 'object_case')); }
sub print_project_words(@project_words) { print_project_word($_) for @project_words; }

1;
