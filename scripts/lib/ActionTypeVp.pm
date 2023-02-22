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
use Utils;
use Word;

package ActionTypeVp;

sub collect_subordinate_clause($sclause, $graph, $i, @stop) {
    for my $id (map { Word::id($_) } grep { !Conjunction::is_conjunction_word($graph, $_) } Graph::get_radj($graph, $i)) {
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

# Skip over "cop" and "case" deprels. Also "mark.
sub not_clause_start($word) { return Word::is_cop($word) || Word::is_case($word) || Word::is_mark($word); }

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
    ActionType::add_value($action_type, $vp, join(" ", map { Word::form($_) } grep { !Word::is_punct($_) } map { Graph::get_word($graph, $_) } Utils::intsort $_->@*));
}

sub process_vp($action_type, $graph, $clause_graph, $verb_id) {
    # Check if clause can be further split via subordinating conjunctions to subordinate clauses, and collect them.
    my @sclauses = get_subordinate_clauses($graph, map { get_sconj_head($graph, $_) } grep { get_sconj(Graph::get_word($graph, $_)) } $clause_graph->{$verb_id}->{'word_ids'}->@*);
    add_sclause_vp($action_type, $graph, $_, $verb_id) for @sclauses;
    
    return;

# skip midvp constructions

    # Check simpler "one-word" vps.
    my @bad_ids = map { $_->@* } @sclauses;
    my (@pre_stuff, @post_stuff);
    for my $id ($clause_graph->{$verb_id}->@*) {
        next if grep { $id == $_ } @bad_ids;
        my $word = Graph::get_word($graph, $id);
        # ADV's handled simpler
        if (Word::is_adv($word) || Word::is_adp($word)) {
            my $arr = ($id < $verb_id ? \@pre_stuff : \@post_stuff);
            push $arr->@*, $id;
            my $head = Word::head($word);
            my $head_word = Graph::get_word($graph, $head);
            #
            if (Word::is_obl($head_word)) {
                push $arr->@*, $head;
                my @conjs = Graph::get_radj_ids_if($graph, $head, \&Word::is_conj);
                my @cconjs = map { Graph::get_radj_if($graph, $_, \&Word::is_cconj) } @conjs;
                push $arr->@*, Word::head($_) for @cconjs;
            }
            #
            if (Word::is_acl($head_word)) {
                push $arr->@*, $head;
                my @nsubjs = Graph::get_radj_ids_if($graph, $head, \&Word::is_nsubj);
                my @obls = Graph::get_radj_ids_if($graph, $head, \&Word::is_obl);
                push $arr->@*, $_ for @nsubjs;
                push $arr->@*, $_ for @obls;
            }
        }
    }
    if (@pre_stuff) {
        @pre_stuff = Utils::intsort @pre_stuff;
        ActionType::add_value($action_type, 'pre_vp', join(" ", map { Word::form(Graph::get_word($graph, $_)); } $pre_stuff[0]..$pre_stuff[-1]));
    }
    if (@post_stuff) {
        @post_stuff = Utils::intsort @post_stuff;
        ActionType::add_value($action_type, 'post_vp', join(" ", map { Word::form(Graph::get_word($graph, $_)); } $post_stuff[0]..$post_stuff[-1]));
    }

}

1;
