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
use ActionTypeObject;
use ActionTypeSubject;
use ActionTypeVerb;
use ActionTypeVp;
use ClauseGraph;
use Graph;
use Participle;
use Log;
use Score;
use Utils;

package ActionTypeParser;

sub generalize_action_type($action_type) {
    Log::write_out("    Generalized action_type ($action_type->{'subject'}, $action_type->{'verb'}, $action_type->{'object'}).\n");
    $action_type->{'subject'} = Convert::generalize_subject($action_type->{'subject'}) unless ActionType::is_set($action_type, "subject_is_propn");
    $action_type->{'verb'} = Convert::generalize_verb($action_type->{'verb'});
    $action_type->{'object'} = Convert::generalize_object($action_type->{'object'}) unless ActionType::is_set($action_type, "object_is_propn");
}

sub parse_action_types($document, $sentence) {
    my %graph = Graph::graph(Sentence::get_words($sentence));
    my %clause_graph = ClauseGraph::clause_graph(\%graph);

    Log::write_out("Parsing action types in sentence <$sentence->{'text'}>.\n");

    Log::write_out("    Sentence structure:");
    Log::sentence_structure(\%graph);

    Log::write_out("    Sentence clauses:");
    Log::clauses(\%graph, \%clause_graph);

    # Go through clauses in order.
    for my $id (ClauseGraph::get_sorted_clause_node_ids(\%clause_graph)) {
        my $clause_text = Utils::word_ids_to_text(\%graph, $clause_graph{$id}->{'word_ids'}->@*);
        Log::write_out("    Processing clause: $clause_text.\n");

        my $word = Graph::get_word(\%graph, $id);

        unless (Word::is_verb($word)) {
            Log::write_out("    Continue: nonverbal clause root: \"" . Word::form($word) . "\".\n");
            next;
        }

        if (Word::get_feat($word, "VerbForm") eq "Inf") {
            Log::write_out("    Continue: infinitive verb: \"" . Word::form($word) . "\".\n");
            next;
        }

        unless (Participle::check_proper_participle($word)) {
            Log::write_out("    Continue: Unaccepted participle form: \"" . Word::form($word) . "\".\n");
            next;
        }

        # Initialize new action type.
        my $action_type = ActionType::action_type();

        ActionTypeVerb::process_main_verb($action_type, \%graph, $id);

        # Verb must not be linked to open clausal complement verbs.
        my @xcomps = grep { Word::is_verb($_) && Word::is_xcomp($_) } Graph::get_radj(\%graph, $id);
        if (@xcomps) {
            Log::write_out("    Continue: open clausal complement verbs not allowed: \"" . Word::form($word) . "\" -> " . Utils::quoted_word_forms(@xcomps) . ".\n");
            next;
        }

        next unless ActionTypeSubject::process_subject($action_type, \%graph, $id);

        next unless ActionTypeObject::process_object($action_type, \%graph, $id);

        ActionTypeVp::process_vp($action_type, \%graph, \%clause_graph, $id);

        $action_type->{'has_vp'} = "TRUE" if ActionType::is_set($action_type, "pre_vp") || ActionType::is_set($action_type, "post_vp");

        # Generalize action type if "pre_vp" or "post_vp" is set.
        generalize_action_type($action_type) if ActionType::is_set($action_type, "has_vp");

        my @clause_words = map { Graph::get_word(\%graph, $_) } $clause_graph{$id}->{'word_ids'}->@*;
        $action_type->{'score'} = Utils::precision(Score::score_words($document->{'score_keeper'}, @clause_words), 3);
        $action_type->{'global_score'} = Utils::precision(Score::score_words($Score::global_score_keeper, @clause_words), 3);

        $action_type->{'text'} = $clause_text;
        $action_type->{'source'} = $document->{'filename'};
        $action_type->{'action_type_id'} = sprintf("AT%03d_%04d", $document->{'document_id'}, scalar($document->{'action_types'}->@*) + 1);

        Log::write_out("    New action type:");
        Log::action_type($action_type);

        push $document->{'action_types'}->@*, $action_type;
    }
}

1;
