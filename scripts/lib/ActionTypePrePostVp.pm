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

    # Go through word ids in reverse order so that @stop gets filled correctly in most cases.
    for my $id (reverse ClauseGraph::get_sorted_word_ids($clause_graph, $verb_id)) {
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

        my $is_case = Word::is_case($word);
        # Only process cases and fixeds.
        next unless $is_case || Word::is_fixed($word);

        my $head = Word::head($word);
        my $head_word = Graph::get_word($graph, $head);
        next if Utils::contains(\@stop, $head);

        # Adpositional case pointing to pronoun head loses context.
        next if $is_adp && $is_case && Word::is_pron($head_word);

        # Conj constructs too complicated to process here with simple rules.
        next if Word::is_conj($head_word);

        # Don't include proper nouns here.
        next if Word::is_propn($head_word);

        my @content = ($id, $head);

        # Get other connected fixeds, determiners, mods, coordinated conjunctions and aux cops from head's radj.
        my @connected_fixeds = grep { $_ != $id } Graph::get_radj_ids_if($graph, $head, \&Word::is_fixed);
        my @connected_determiners = Graph::get_radj_ids_if($graph, $head, \&Word::is_det);
        my @connected_mods = Graph::get_radj_ids_if($graph, $head, \&Word::is_mod);
        my @ccs = Conjunction::get_coordinated_elements_as_ids($graph, $head_word);
        my @aux_cops = Graph::get_radj_ids_if($graph, $head, \&Word::is_cop); # This includes VERB_cops.
        push @aux_cops, Graph::get_radj_ids_if($graph, $head, \&Word::has_cop) if @aux_cops;
        push @content, grep { !Utils::contains(\@stop, $_) } (@connected_fixeds, @connected_determiners, @connected_mods, @ccs, @aux_cops);
        push @stop, @content;

        my $key = $id < $verb_id ? 'pre_vp' : 'post_vp';
        my $type = $is_adv ? 'adverbial' : 'adpositional';
        my $text = Utils::word_ids_to_text($graph, @content);
        if (grep { !Utils::contains(\@stop, Word::id($_)) } grep { !Word::is_punct($_) } Graph::get_radj($graph, $head)) {
            Log::write_out_indented("Action type: could not parse all content for complicated $type construct: \"" . Word::form(Graph::get_word($graph, $head)) . "\".\n");
            next;
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
