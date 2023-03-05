#!/usr/bin/perl
use warnings;
use strict;
use v5.20;
use utf8;
no warnings "experimental::signatures";
use feature qw(postderef signatures);

use File::Basename;
use lib dirname (__FILE__);

use Conjunction;
use Graph;
use SubordinateClause;
use Utils;
use Word;

package ActionTypeVp;

sub add_sclause_vp($action_type, $graph, $sclause, $verb_id) {
    my $vp = $sclause->[0] < $verb_id ? 'pre_vp' : 'post_vp';
    ActionType::add_value($action_type, $vp, join(" ", map { Word::form($_) } grep { !Word::is_punct($_) } map { Graph::get_word($graph, $_) } Utils::intsort $sclause->@*));
}

sub process_vp($action_type, $graph, $clause_graph, $verb_id) {
    # Check if clause can be further split via subordinating conjunctions to subordinate clauses, and collect them.
    my @sclauses = SubordinateClause::get_subordinate_clauses($graph, $clause_graph, $verb_id);
    my $subject_id = $action_type->{'subject_id'};
    my $object_id = $action_type->{'object_id'};
    for (@sclauses) {
        next if (grep { $_ eq $subject_id || $_ eq $object_id || $_ eq $verb_id } $_->@*);
        add_sclause_vp($action_type, $graph, $_, $verb_id) 
    }
    
    # More vp types to be processed soon.

    return;

}

1;
