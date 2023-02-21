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

my $fh;

sub open_and_clear_log($execname, $logfile) {
    open($fh, '>>', $logfile) or die "$execname: can't open '$logfile'.";
    truncate($fh, 0) or die "$execname: can't clear '$logfile'.";
}

sub close_log() { close($fh); }

sub write_out($str) { say $fh $str or die $!; }

sub hr() { write_out("    " . "-" x 80); }
sub br() { write_out(""); }

sub sentence_structure($graph) {
    hr();
    # Go through the sentence's reverse dependency graph recursively and print out the nodes.
    my @stack = (Graph::get_root_id($graph), 0);
    while (@stack) {
        my ($depth, $id) = (pop @stack, pop @stack);
        my $word = Graph::get_word($graph, $id);
        write_out("    " . "      " x $depth . Word::form($word) . "  " . Word::upos($word) . '_' . Word::deprel($word));
        ++$depth;
        push @stack, $_, $depth for Utils::intsort Graph::get_radj_ids($graph, $id);
    }
    hr();
    br();
}

sub clauses($graph, $clauses) {
    hr();
    write_out("    " . Utils::word_ids_to_text($graph, Utils::intsort $clauses->{$_}->@*)) for Utils::intsort keys %$clauses;
    hr();
    br();
}

sub action_type($action_type) {
    write_out(sprintf "    %30s   %s", $_, $action_type->{$_}) for @ActionType::action_type_field_names;
    br();
}

sub project_words($project_words) {
    write_out(sprintf "    %30s   %s", $_, $project_words->{$_}) for @ProjectWords::project_words_field_names;
    br();
}

1;
