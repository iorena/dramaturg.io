#!/usr/bin/perl
use warnings;
use strict;
use v5.20;
use utf8;
no warnings "experimental::signatures";
use feature qw(postderef signatures);

use File::Basename;
use lib dirname (__FILE__);

package SubordinateClause;

# Marks (which are usually also SCONJs) also work for our purposes.
sub is_sconj_or_mark($word) { return Word::is_sconj($word) || Word::is_mark($word); }

# Copula, case marking or marker.
sub is_cop_case_or_mark($word) { return Word::is_cop($word) || Word::is_case($word) || Word::is_mark($word); }

sub collect_subordinate_clause($sclause, $graph, $i, $stop) {
    for my $id (map { Word::id($_) } grep { !Conjunction::is_conjunction_word($graph, $_) } Graph::get_radj($graph, $i)) {
        if (!grep { $_ eq $id } $stop->@*) {
            push $sclause->@*, $id;
            push $stop->@*, $id;
            collect_subordinate_clause($sclause, $graph, $id, $stop);
        }
    }
}

# Ascend the graph via head word(s) until we reach the level at which the subordinate clause starts.
sub get_subordinate_clause_ids($graph, $sconj_id) {
    do {
        # Ascend at least once.
        $sconj_id = Word::head(Graph::get_word($graph, $sconj_id));
    } while ($sconj_id > 0 && is_cop_case_or_mark(Graph::get_word($graph, $sconj_id)));

    return $sconj_id;
}

sub get_subordinate_clauses($graph, $clause_graph, $verb_id) {
    # Look for subordinating conjunctions.
    my @sconjs = grep { is_sconj_or_mark(Graph::get_word($graph, $_)) } $clause_graph->{$verb_id}->{'word_ids'}->@*;

    # Find the ids of the head word(s) of the subordinate clauses.
    my @sclause_ids = map { get_subordinate_clause_ids($graph, $_) } @sconjs;

    my @sclauses;
    my @stop;

    for my $sclause_id (@sclause_ids) {
        next if grep { $_ eq $sclause_id } @stop;
        push @stop, $sclause_id;
        my @sclause = ($sclause_id);
        collect_subordinate_clause(\@sclause, $graph, $sclause_id, \@stop);
        push @sclauses, \@sclause;
    }

    return @sclauses;
}



1;
