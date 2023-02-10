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
use Graph;
use ProjectWords;
use Utils;
use Word;

package Log;

our $execname = "";
our $logfile = "";

sub open_log() {
    open(my $fh, '>>', $logfile) or die "$execname: can't open '$logfile' for clearing.";
    return $fh;
}

sub clear_log() {
    my $fh = open_log();
    truncate($fh, 0) or die "$execname: can't clear '$logfile'.";
    close($fh);
}

sub message($str) {
    my $fh = open_log();
    say $fh $str;
    close($fh);
}

sub sentence_structure($graph) {
    my $fh = open_log();

    say $fh "    " . "-" x 80;

    # Go through the sentence's reverse dependency graph recursively and print out the nodes.
    my @stack = (Graph::get_root_id($graph), 0);
    while (@stack) {
        my ($depth, $id) = (pop @stack, pop @stack);
        my $word = Graph::get_word($graph, $id);
        say $fh "    " . "      " x $depth . Word::form($word) . "  " . Word::upos($word) . '_' . Word::deprel($word);
        ++$depth;
        push @stack, $_, $depth for Utils::intsort Graph::get_radj_ids($graph, $id);
    }

    say $fh "    " . "-" x 80 . "\n";

    close($fh);
}

sub clauses($graph, $clauses) {
    my $fh = open_log();
    say $fh "    " . "-" x 80;
    say $fh "    " . Utils::word_ids_to_text($graph, Utils::intsort $clauses->{$_}->@*) for Utils::intsort keys %$clauses;
    say $fh "    " . "-" x 80 . "\n";
    close($fh);
}

sub action_type($action_type) {
    my $fh = open_log();
    printf $fh "    %30s   %s\n", $_, $action_type->{$_} for @ActionType::action_type_field_names;
    say $fh "";
    close($fh);
}

sub project_words($project_words) {
    my $fh = open_log();
    printf $fh "    %30s   %s\n", $_, $project_words->{$_} for @ProjectWords::project_words_field_names;
    say $fh "";
    close($fh);
}

1;
