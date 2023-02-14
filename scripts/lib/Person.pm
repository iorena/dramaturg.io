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

# Encode singular forms as 1, 2 and 3, plural forms as 4, 5 and 6.
sub get_person_number($person, $number) { return $person ? ($number eq "Plur" ? $person + 3 : $person) : undef; }

# Accept encoded persons 1-5.
sub valid_person($person) { return $person && $person ne "6"; }

# According to CoNLL-U rules, Reflex feat is only set when Reflex=Yes and in such cases the PronType feat is implicitly PronType=Prs.
# Thus, it would suffice to only check for the presence of PronType=Prs, but for clarity/future-proofing both are checked here.
sub is_nonreflexive_personal_pronoun($word) {
    return Word::is_pron($word)
        && Word::get_feat($word, "PronType") eq "Prs"
        && Word::get_feat($word, "Reflex") ne "Yes";
}

# Get feats required to identify person. Person[psor] not used with current criteria.
sub get_person($word) { return get_person_number(Word::get_feats($word, ("Person", "Number"))); }
# sub get_person_psor($word) { return get_person_number(Word::get_feats($word, ("Person[psor]", "Number[psor]"))); }

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

# Converts word to person form if it is nonreflexive personal pronoun and predicate returns true,
# otherwise returns Word::form (proper nouns capitalized, lower case otherwise).
sub form_or_person_if($word, $predicate) {
    if ($predicate->($word) && is_nonreflexive_personal_pronoun($word)) {
        my $person = get_person($word);
        return Convert::person($person) if valid_person($person);
    }
    return Word::is_propn($word) ? Word::form($word) : Utils::lower_case(Word::form($word));
}

# Converts word to person form if it is nonreflexive personal pronoun and predicate returns true,
# otherwise returns Word::lemma (with compound-word-indicating hashtags removed).
sub lemma_or_person_if($word, $predicate) {
    if ($predicate->($word) && is_nonreflexive_personal_pronoun($word)) {
        my $person = get_person($word);
        return Convert::person($person) if valid_person($person);
    }
    return Utils::remove_hashtag(Word::lemma($word));
}

1;
