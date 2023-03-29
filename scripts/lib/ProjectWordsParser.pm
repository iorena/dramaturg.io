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
use Participle;
use Log;
use ProjectWords;
use Score;
use Utils;

package ProjectWordsParser;

# Get word (reverse) adjacent to verb of a given type (determined by predicate).
sub get_radj_word($graph, $verb_id, $predicate, $print_type) {
    my @matching_words = Graph::get_radj_if($graph, $verb_id, $predicate);

    unless (@matching_words > 0) {
        Log::write_out_indented("Continue: no $print_type word found.\n");
        return 0;
    }

    unless (@matching_words == 1) {
        Log::write_out_indented("Continue: multiple $print_type words found: " . Utils::quoted_word_forms(@matching_words) . ".\n");
        return 0;
    }
    return $matching_words[0];
}

# Checks that the subject/object is not dependent on any (reverse) adjacent words. 
sub is_standalone_word($graph, $word) {
    my @bad_deprel_predicates = (\&Word::is_flat, \&Word::is_det, \&Word::is_fixed, \&Word::is_gobj, \&Word::is_poss, \&Word::is_cconj);
    for (@bad_deprel_predicates) {
        if (Graph::get_radj_ids_if($graph, Word::id($word), $_)) {
            Log::write_out_indented("Continue: not stand-alone word: \"" . Word::form($word) . "\".\n");
            return 0;
        }
    }
    return 1;
}

sub parse_project_words($document, $sentence) {
    my %graph = Graph::graph(Sentence::get_words($sentence));

    Log::write_out("Parsing project words in sentence <$sentence->{'text'}>.\n");

    Log::write_out_indented("Sentence structure:");
    Log::sentence_structure(\%graph);
    
    my @words = grep { Word::is_verb($_) && Conjunction::is_conjunction_word(\%graph, $_) && Participle::check_proper_participle($_) } Sentence::get_words($sentence);

    Log::write_out_indented("Continue: no proper verbs found.\n") unless @words;

    for my $word (@words) {
        Log::write_out_indented("Processing verb \"" . Word::form($word) . "\".\n");

        my $id = Word::id($word);

        my @xcomps = grep { Word::is_verb($_) && Word::is_xcomp($_) } Graph::get_radj(\%graph, $id);
        if (@xcomps) {
            Log::write_out_indented("Continue: open clausal complement verbs not allowed: \"" . Word::form($word) . "\" -> " . Utils::quoted_word_forms(@xcomps) . ".\n");
            next;
        }

        my @aux = grep { Word::is_aux($_) } Graph::get_radj(\%graph, $id);
        if (@aux) {
            Log::write_out_indented("Continue: auxiliary verbs not allowed: \"" . Word::form($word) . "\" -> " . Utils::quoted_word_forms(@aux) . ".\n");
            next;
        }

        my $project_words = ActionType::action_type();
        $project_words->{'verb'} = Word::lemma($word);
        $project_words->{'score'} = Score::score_word($document->{'score_keeper'}, $word);

        my $subject_word = get_radj_word(\%graph, $id, \&Word::is_nsubj, "subject");
        next unless $subject_word;

        $project_words->{'subject'} = Word::form($subject_word);

        my $object_word = get_radj_word(\%graph, $id, \&Word::is_obj, "object");
        next unless $object_word;

        if (Word::is_pron($object_word)) {
            Log::write_out_indented("Continue: pronoun object not allowed: \"" . Word::form($object_word) . "\".\n");
            next;
        }

        if (Word::is_adj($object_word)) {
            Log::write_out_indented("Continue: adjective object not allowed: \"" . Word::form($object_word) . "\".\n");
            next;
        }

        next unless is_standalone_word(\%graph, $subject_word) && is_standalone_word(\%graph, $object_word);

        $project_words->{'object'} = Utils::remove_hashtag(Word::lemma($object_word));
        $project_words->{'object_case'} = Word::get_feat($object_word, "Case");

        $project_words->{'score'} = Utils::precision(Score::score_words($document->{'score_keeper'}, ($word, $subject_word, $object_word)), 3);

        Log::write_out_indented("New project words:");
        Log::project_words($project_words);

        push $document->{'project_words'}->@*, $project_words;
    }
}

1;
