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
use Output;
use Score;
use Utils;

package ActionTypeParser;

sub parse_action_types($document, $sentence) {
    my %graph = Graph::graph($sentence);
    my %clauses = Clause::get_clauses(\%graph);

    Output::log_msg("Parsing action types in sentence <$sentence->{'text'}>.\n");

    Output::log_msg("    Sentence structure:");
    Output::log_sentence_structure(\%graph);

    Output::log_msg("    Sentence clauses:");
    Output::log_clauses(\%graph, \%clauses);

    # Go through clauses in order.
    for my $id (Utils::intsort keys %clauses) {
        my $clause_text = Utils::word_ids_to_text(\%graph, $clauses{$id}->@*);
        Output::log_msg("    Processing clause: $clause_text.");

        my $word = Graph::get_word(\%graph, $id);

        unless (Word::is_verb($word)) {
            Output::log_msg("    Continue: nonverbal clause.\n");
            next;
        }

        unless (Participle::check_proper_participle($word)) {
            Output::log_msg("    Continue: Unaccepted participle form.\n");
            next;
        }

        # Initialize new action type.
        my $action_type = ActionType::action_type();

        ActionTypeVerb::process_main_verb($action_type, \%graph, $id);

        if (grep { Word::is_verb($_) && Word::is_xcomp($_) } Graph::get_radj(\%graph, $id)) {
            Output::log_msg("    Continue: open clausal complement verbs not allowed.\n");
            next;
        }

        next unless ActionTypeSubject::process_subject($action_type, \%graph, $id);

        next unless ActionTypeObject::process_object($action_type, \%graph, $id);

        ActionTypeVp::process_vp($action_type, \%graph, \%clauses, $id);

        my @clause_words = map { Graph::get_word(\%graph, $_) } $clauses{$id}->@*;
        $action_type->{'score'} = Utils::precision(Score::score_words($document->{'score_keeper'}, @clause_words), 3);
        $action_type->{'global_score'} = Utils::precision(Score::score_words($Score::global_score_keeper, @clause_words), 3);

        $action_type->{'text'} = $clause_text;
        $action_type->{'source'} = $document->{'filename'};
        $action_type->{'action_type_id'} = "AT" . sprintf("%03d", $document->{'document_id'}) . '_' . sprintf("%04d", scalar($document->{'action_types'}->@*) + 1);

        Output::log_msg("    New action type:");
        Output::log_action_type($action_type);

        push $document->{'action_types'}->@*, $action_type;
    }
}

1;
