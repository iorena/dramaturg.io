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
use Utils;
use Word;

package Person;

sub valid_person($person) { return $person && $person ne "6"; }

# Encode singular forms as 1, 2 and 3, plural forms as 4, 5 and 6.
sub get_person_number($person, $number) { return $person ? ($number eq "Plur" ? $person + 3 : $person) : undef; }

# According to CoNLL-U rules, Reflex feat is only set when Reflex=Yes
# and in such cases the PronType feat is not set (but is implied as PronType=Prs).
# Thus, it would suffice to only check for the presence of PronType=Prs,
# but for future-proofing reasons both are checked here.
sub is_nonreflexive_personal_pronoun($word) {
    return Word::is_pron($word)
        && Word::get_feat($word, "PronType") eq "Prs"
        && Word::get_feat($word, "Reflex") ne "Yes";
}

# Get person or person of possessor.
sub get_person($word) { return get_person_number(Word::get_feats($word, ("Person", "Number"))); }
sub get_person_psor($word) { return get_person_number(Word::get_feats($word, ("Person[psor]", "Number[psor]"))); }

# Attempt to get (implicit) person through the verb's "Person" feat.
sub get_implicit_person_from_verb($graph, $verb_id) {
    my $person = get_person(Graph::get_word($graph, $verb_id));
    if (!$person) {
        # Check auxiliary verbs.
        for (Graph::get_radj_if($graph, $verb_id, \&Word::is_aux)) {
            $person = get_person($_) if !$person;
        }
    }
    return $person;
}

# These subroutines will convert pronouns 
# Predicate will separate the checked word from others.

# Fix these comments
# Convert word to person form if word is a pron/person, otherwise return normal form.
sub form_or_person_if($word, $predicate) {
    if (is_nonreflexive_personal_pronoun($word) && $predicate->($word)) {
        my $person = get_person_psor($word);
        return Convert::person($person) if valid_person($person);
    }
    return Word::form($word);
}

# Convert word to person form if word is a pronperson, otherwise return normal lemma.
sub lemma_or_person_if($word, $predicate) {
    if (is_nonreflexive_personal_pronoun($word) && $predicate->($word)) {
        my $person = get_person_psor($word);
        return Convert::person($person) if valid_person($person);
    }
    return Utils::remove_hashtag(Word::lemma($word));
}

1;
