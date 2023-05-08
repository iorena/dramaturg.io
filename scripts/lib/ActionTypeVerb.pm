#!/usr/bin/perl
use warnings;
use strict;
use v5.20;
use utf8;
no warnings "experimental::signatures";
use feature qw(postderef signatures);

use File::Basename;
use lib dirname (__FILE__);

use Convert;
use Graph;
use Word;

package ActionTypeVerb;

# Deduces Finnish tense from the universal features "VerbForm" and "Tense".
sub get_finnish_tense($verbform, $tense) { return ($verbform eq "Part" ? ($tense eq "Pres" ? "Perf" : "Pluperf") : $tense); }

sub process_main_verb($action_type, $graph, $verb_id) {
    my $word = Graph::get_word($graph, $verb_id);
    return unless Word::is_verb($word);
    my $id = Word::id($word);
    $action_type->{'verb'} = Word::lemma($word);

    # Set feats readable from verb itself.
    my ($mood, $tense, $clitic, $voice, $verbform, $number, $person) = Word::get_feats($word, ("Mood", "Tense", "Clitic", "Voice", "VerbForm", "Number", "Person"));
    $action_type->{'interrogative_form'} = "TRUE" if $clitic eq "Ko";
    $action_type->{'passive_form'} = "TRUE" if $voice eq "Pass";

    # If mood and tense are not set here, they are specified by the auxiliary verb, to be processed next.
    $action_type->{'modus'} = Convert::mood($mood) if $mood;
    $action_type->{'tense'} = Convert::tense($tense) if $tense; # Will only set "Tense" here if "VerbForm" is not set.

    # Read feats from words connected to verb.
    for (Graph::get_radj($graph, $id)) {
        $action_type->{'interrogative_form'} = "TRUE" if (Word::get_feat($_, "Clitic") eq "Ko");
        $action_type->{'negative_form'} = "TRUE" if (Word::get_feat($_, "Polarity") eq "Neg");
        if (Word::is_aux($_)) {
            my ($mood, $tense) = Word::get_feats($_, ("Mood", "Tense"));
            $action_type->{'modus'} = Convert::mood($mood) if $mood;
            $action_type->{'tense'} = Convert::tense(get_finnish_tense($verbform, $tense)) if $tense;
            ActionType::add_value($action_type, "auxiliary_verb", Word::lemma($_));
        }
    }
}

1;
