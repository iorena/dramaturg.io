#!/usr/bin/perl
use warnings;
use strict;
use v5.20;
use utf8;
no warnings "experimental::signatures";
use feature qw(postderef signatures);

use File::Basename;
use lib dirname (__FILE__);

use Clause;
use Graph;
use Utils;
use Word;

package ActionTypeVp;

sub collect_subordinate_clause($sclause, $graph, $i, @stop) {
    for my $id (map { Word::id($_) } grep { !Clause::starts_new_clause($_) } Graph::get_radj($graph, $i)) {
        if (!grep { /^$id$/ } @stop) {
            push @{$sclause}, $id;
            collect_subordinate_clause($sclause, $graph, $id, @stop);
        }
    }
}

sub get_subordinate_clauses($graph, @sconj_heads) {
    my @sclauses;
    for (@sconj_heads) {
        my @sclause = ($_);
        collect_subordinate_clause(\@sclause, $graph, $_, @sconj_heads);
        push @sclauses, \@sclause;
    }
    return @sclauses;
}

# Skip over "cop" and "case" deprels.
sub not_clause_start($word) { return Word::is_cop($word) || Word::is_case($word); }

# Get "SCONJ" "HEAD" to point to clause start.
sub get_sconj_head($graph, $sconj_id) {
    do {
        $sconj_id = Word::head(Graph::get_word($graph, $sconj_id));
    } while ($sconj_id > 0 && not_clause_start(Graph::get_word($graph, $sconj_id)));
    return $sconj_id;
}

# Can be checked via "SCONJ" UPOS or "mark" DEPREL. The former is usually also the latter.
sub get_sconj($word) { return Word::is_sconj($word) || Word::is_mark($word); }

sub add_sclause_vp($action_type, $graph, $sclause, $verb_id) {
    my $vp = $sclause->[0] < $verb_id ? 'pre_vp' : 'post_vp';
    ActionType::add_value($action_type, $vp, join(' ', map { Word::form($_) } grep { !Word::is_punct($_) } map { Graph::get_word($graph, $_) } Utils::intsort $_->@*));
}

sub process_vp($action_type, $graph, $clauses, $verb_id) {
    # Check if clause can be further split via subordinating conjunctions to subordinate clauses, and collect them.
    my @sclauses = get_subordinate_clauses($graph, map { get_sconj_head($graph, $_) } grep { get_sconj(Graph::get_word($graph, $_)) } $clauses->{$verb_id}->@*);
    add_sclause_vp($action_type, $graph, $_, $verb_id) for @sclauses;
    
    # Check simpler "one-word" vps.
    my @bad_ids = map { $_->@* } @sclauses;
    my (@pre_stuff, @post_stuff);
    for my $id ($clauses->{$verb_id}->@*) {
        next if grep { /$id/ } @bad_ids;
        my $word = Graph::get_word($graph, $id);
        if (Word::is_adv($word) || Word::is_adp($word)) {
            if ($id < $verb_id) {
                push @pre_stuff, $id;
            } else {
                push @post_stuff, $id;
            }
        }
    }
    if (@pre_stuff) {
        ActionType::add_value($action_type, 'pre_vp', join(' ', map { Word::lemma(Graph::get_word($graph, $_)); } Utils::intsort @pre_stuff));
    }
    if (@post_stuff) {
        ActionType::add_value($action_type, 'post_vp', join(' ', map { Word::lemma(Graph::get_word($graph, $_)); } Utils::intsort @post_stuff));
    }

}

1;
