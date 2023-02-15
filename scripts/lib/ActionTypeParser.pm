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
use Clause;
use Graph;
use Participle;
use Log;
use Score;
use Utils;

package ActionTypeParser;

sub generalize_action_type($action_type) {
    Log::message("    Generalized action_type ($action_type->{'subject'}, $action_type->{'verb'}, $action_type->{'object'}).\n");
    $action_type->{'subject'} = Convert::generalize_subject($action_type->{'subject'}) unless exists $action_type->{'subject_is_propn'};
    $action_type->{'verb'} = Convert::generalize_verb($action_type->{'verb'});
    $action_type->{'object'} = Convert::generalize_object($action_type->{'object'}) unless exists $action_type->{'object_is_propn'};
}

sub parse_action_types($document, $sentence) {
    my %graph = Graph::graph($sentence);
    my %clauses = Clause::get_clauses(\%graph);

    Log::message("Parsing action types in sentence <$sentence->{'text'}>.\n");

    Log::message("    Sentence structure:");
    Log::sentence_structure(\%graph);

    Log::message("    Sentence clauses:");
    Log::clauses(\%graph, \%clauses);

    # Go through clauses in order.
    for my $id (Utils::intsort keys %clauses) {
        my $clause_text = Utils::word_ids_to_text(\%graph, $clauses{$id}->@*);
        Log::message("    Processing clause: $clause_text.\n");

        my $word = Graph::get_word(\%graph, $id);

        unless (Word::is_verb($word)) {
            Log::message("    Continue: nonverbal clause.\n");
            next;
        }

        if (Word::get_feat($word, "VerbForm") eq "Inf") {
            Log::message("    Continue: infinitive verb.\n");
            next;
        }

        unless (Participle::check_proper_participle($word)) {
            Log::message("    Continue: Unaccepted participle form.\n");
            next;
        }

        # Initialize new action type.
        my $action_type = ActionType::action_type();

        ActionTypeVerb::process_main_verb($action_type, \%graph, $id);

        # Verb must not be linked to open clausal complement verbs.
        if (grep { Word::is_verb($_) && Word::is_xcomp($_) } Graph::get_radj(\%graph, $id)) {
            Log::message("    Continue: open clausal complement verbs not allowed.\n");
            next;
        }

        next unless ActionTypeSubject::process_subject($action_type, \%graph, $id);

        next unless ActionTypeObject::process_object($action_type, \%graph, $id);

        ActionTypeVp::process_vp($action_type, \%graph, \%clauses, $id);

        $action_type->{'has_vp'} = "TRUE" if ActionType::is_set($action_type, "pre_vp") || ActionType::is_set($action_type, "post_vp");

        # Generalize action type if "pre_vp" or "post_vp" is set.
        generalize_action_type($action_type) if ActionType::is_set($action_type, "has_vp");

        my @clause_words = map { Graph::get_word(\%graph, $_) } $clauses{$id}->@*;
        $action_type->{'score'} = Utils::precision(Score::score_words($document->{'score_keeper'}, @clause_words), 3);
        $action_type->{'global_score'} = Utils::precision(Score::score_words($Score::global_score_keeper, @clause_words), 3);

        $action_type->{'text'} = $clause_text;
        $action_type->{'source'} = $document->{'filename'};
        $action_type->{'action_type_id'} = sprintf("AT%03d_%04d", $document->{'document_id'}, scalar($document->{'action_types'}->@*) + 1);

        Log::message("    New action type:");
        Log::action_type($action_type);

        push $document->{'action_types'}->@*, $action_type;
    }
}

1;
