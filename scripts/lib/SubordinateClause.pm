#!/usr/bin/perl
use warnings;
use strict;
use v5.20;
use utf8;
no warnings "experimental::signatures";
use feature qw(postderef signatures);

use File::Basename;
use lib dirname (__FILE__);

use Utils;

use List::MoreUtils;

package SubordinateClause;

# Marks (which are usually also SCONJs) also work for our purposes.
sub is_sconj_or_mark($word) { return Word::is_sconj($word) || Word::is_mark($word); }

# Copula, case marking or marker.
sub is_cop_case_or_mark($word) { return Word::is_cop($word) || Word::is_case($word) || Word::is_mark($word); }

sub collect_subordinate_clause($sclause, $graph, $i, $stop) {
    for my $id (map { Word::id($_) } grep { !Conjunction::is_conjunction_word($graph, $_) } Graph::get_radj($graph, $i)) {
        if (!Utils::contains($stop, $id)) {
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
    my @sconjs = grep { is_sconj_or_mark(Graph::get_word($graph, $_)) } ClauseGraph::get_sorted_word_ids($clause_graph, $verb_id);

    # Find the ids of the head word(s) of the subordinate clauses.
    my @sclause_ids = map { get_subordinate_clause_ids($graph, $_) } @sconjs;

    # Search might've set verb as a head word - remove it.
    @sclause_ids = grep { $_ != $verb_id } @sclause_ids;

    # Remove duplicates.
    @sclause_ids = List::MoreUtils::uniq(@sclause_ids);

    # Sort so that the next search starts from the lowest depth.
    @sclause_ids = sort { $graph->{$a}->{'depth'} <=> $graph->{$b}->{'depth'} } @sclause_ids;

    # Note: initializing with empty @stop and checking $sclause_ids against @stop below will join hierarchical
    # subordinate clauses together. This works better because subordinating conjunctions tend to be work together to be logically meaningful.
    # The alternative implementation would set @stop = @sclause_ids and disable the @stop checks below.
    my @stop;
    my @sclauses;

    for my $sclause_id (@sclause_ids) {
        next if Utils::contains(\@stop, $sclause_id);
        push @stop, $sclause_id;
        my @sclause = ($sclause_id);
        collect_subordinate_clause(\@sclause, $graph, $sclause_id, \@stop);
        push @sclauses, \@sclause;
    }

    return @sclauses;
}



1;
