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
use Log;
use SubordinateClause;
use Utils;
use Word;

package ActionTypePrePostVp;

sub process_prepostvp($action_type, $graph, $clause_graph, $verb_id) {
    # Check if clause can be further split via subordinating conjunctions to subordinate clauses, and collect them.
    my @sclauses = SubordinateClause::get_subordinate_clauses($graph, $clause_graph, $verb_id);

    # Track used ids.
    my @stop = ($verb_id, $action_type->{'subject_id'}, $action_type->{'object_id'});

    for my $sclause (@sclauses) {
        next if Utils::contains($sclause, @stop);
        push @stop, $sclause->@*;
        my $key = $sclause->[0] < $verb_id ? 'pre_vp' : 'post_vp';
        my $text = Utils::word_ids_to_text($graph, grep { !Word::is_punct(Graph::get_word($graph, $_)) } $sclause->@*);
        ActionType::add_value($action_type, $key, $text);
        Log::write_out_indented("Action type: add '$key' subordinate clause: \"$text\".\n");
    }

    # Check simpler constructs from adpositions and adverbials.
    my @discourses;

    # Maybe go through clause nodes?
    for my $id (ClauseGraph::get_sorted_word_ids($clause_graph, $verb_id)) {
        next if Utils::contains(\@stop, $id);
        my $word = Graph::get_word($graph, $id);
        my $is_adv = Word::is_adv($word);
        if (($is_adv || Word::is_intj($word)) && Word::is_discourse($word)) {
            # Store discourses for later processing.
            push @discourses, $id;
            next;
        }
        my $is_adp = Word::is_adp($word);
        next unless $is_adv || $is_adp;
        next unless Word::is_case($word) || Word::is_fixed($word);
        my $head = Word::head($word);
        next if Utils::contains(\@stop, $head);
        my @content = ($id, $head);
        # Get other fixeds.
        push @content, grep { $_ != $id } Graph::get_radj_ids_if($graph, $head, \&Word::is_fixed);
        push @stop, @content;
        my $key = $id < $verb_id ? 'pre_vp' : 'post_vp';
        my $type = $is_adv ? 'adverbial' : 'adpositional';
        my $text = Utils::word_ids_to_text($graph, @content);
        if (scalar(@content) - 1 != scalar(Graph::get_radj($graph, $head))) {
            Log::write_out_indented("Action type: detected complicated $type construct: subgraph from \"" . Word::form(Graph::get_word($graph, $head)) . "\" larger than expected.\n");
        }
        ActionType::add_value($action_type, $key, $text);
        Log::write_out_indented("Action type: add '$key' $type construct: \"$text\".\n");
    }

    # Get unused discourses and sort.
    @discourses = grep { !Utils::contains(\@stop, $_) } Utils::intsort @discourses;
    # Require discourses to be next to each other.
    if (@discourses && $discourses[$#discourses] - $discourses[0] != $#discourses) {
        my $key = $discourses[$#discourses] < $verb_id ? 'pre_vp' : 'post_vp';
        my $text = Utils::word_ids_to_text($graph, @discourses);
        ActionType::add_value($action_type, $key, $text);
        Log::write_out_indented("Action type: add '$key' adverbial discourse construct: \"$text\".\n");
    }
    

}

1;
