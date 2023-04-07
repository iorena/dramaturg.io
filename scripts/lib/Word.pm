#!/usr/bin/perl
use warnings;
use strict;
use v5.20;
use utf8;
no warnings "experimental::signatures";
use feature qw(postderef signatures);

package Word;

# Create a word hash which stores the needed fields from a CoNLL-U word line.
sub word($id, $form, $lemma, $upos, $feats, $head, $deprel) {
    return {
        'ID' => $id,
        'FORM' => $form,
        'LEMMA' => $lemma,
        'UPOS' => $upos,
        'FEATS' => $feats,
        'HEAD' => $head,
        'DEPREL' => $deprel
    };
}

# Parse fields from a CoNLL-U word line.
sub parse_word_line($word_line) {
    my ($id, $form, $lemma, $upos, undef, $feats, $head, $deprel) = split('\t', $word_line);
    return word($id, $form, $lemma, $upos, $feats, $head, $deprel);
}

# Get parts from compound word.
sub get_word_parts($word) { return split('#', lemma($word)); }

# Get the "basic type" or subtype from universal syntactic relation.
sub baseform($x) { return $x =~ s/:.*//r; } # Remove subtype from deprel.
sub subtype($x) { return $x =~ m/:/ ? $x =~ s/.*://r : ""; } # Remove baseform from deprel; return empty if deprel has no subtype.

# Accessors for the CoNLL-U fields.
sub id($word) { return $word->{'ID'}; }
sub form($word) { return $word->{'FORM'}; }
sub lemma($word) { return $word->{'LEMMA'}; }
sub feats($word) { return $word->{'FEATS'}; }
sub head($word) { return $word->{'HEAD'}; }
sub upos($word) { return $word->{'UPOS'}; }
sub deprel($word) { return $word->{'DEPREL'}; }

# Queries about the CoNLL-U UPOS field.
sub is_verb($word) { return upos($word) eq "VERB"; }
sub is_noun($word) { return upos($word) eq "NOUN"; }
sub is_pron($word) { return upos($word) eq "PRON"; }
sub is_propn($word) { return upos($word) eq "PROPN"; }
sub is_adj($word) { return upos($word) eq "ADJ"; }
sub is_adv($word) { return upos($word) eq "ADV"; }
sub is_adp($word) { return upos($word) eq "ADP"; }
sub is_punct($word) { return upos($word) eq "PUNCT"; }
sub is_sconj($word) { return upos($word) eq "SCONJ"; } # Not to be confused with the DEPREL "conj".
sub is_cconj($word) { return upos($word) eq "CCONJ"; } # Not to be confused with the DEPREL "conj".
sub is_intj($word) { return upos($word) eq "INTJ"; }

# Queries about the CoNLL-U deprel field.
sub is_aux($word) { return baseform(deprel($word)) eq "aux"; } # Not to be confused with the UPOS "AUX".
sub is_nsubj($word) { return baseform(deprel($word)) eq "nsubj" };
sub is_obj($word) { return baseform(deprel($word)) eq "obj"; }
sub is_root($word) { return baseform(deprel($word)) eq "root"; }
sub is_conj($word) { return baseform(deprel($word)) eq "conj"; }
sub is_parataxis($word) { return baseform(deprel($word)) eq "parataxis"; }
sub is_ccomp($word) { return baseform(deprel($word)) eq "ccomp"; }
sub is_xcomp($word) { return baseform(deprel($word)) eq "xcomp"; }
sub is_compound($word) { return baseform(deprel($word)) eq "compound"; }
sub is_flat($word) { return baseform(deprel($word)) eq "flat"; }
sub is_acl($word) { return baseform(deprel($word)) eq "acl"; }
sub is_advcl($word) { return baseform(deprel($word)) eq "advcl"; }
sub is_nummod($word) { return deprel($word) eq "nummod"; }
sub is_nmod($word) { return deprel($word) eq "nmod"; }
sub is_mod($word) { index(deprel($word), "mod") != -1; }
sub is_cop($word) { return baseform(deprel($word)) eq "cop"; }
sub is_case($word) { return baseform(deprel($word)) eq "case"; }
sub is_mark($word) { return baseform(deprel($word)) eq "mark"; }
sub is_det($word) { return baseform(deprel($word)) eq "det"; }
sub is_fixed($word) { return baseform(deprel($word)) eq "fixed"; }
sub is_obl($word) { return baseform(deprel($word)) eq "obl"; }
sub is_cc($word) { return baseform(deprel($word)) eq "cc"; }
sub is_discourse($word) { return baseform(deprel($word)) eq "discourse"; }
sub has_gobj($word) { return subtype(deprel($word)) eq "gobj"; }
sub has_poss($word) { return subtype(deprel($word)) eq "poss"; }
sub has_cop($word) { return subtype(deprel($word)) eq "cop"; }

# Accessors for the CoNLL-U field FEATS (list of morphological features from the universal feature inventory).
sub get_feat($word, $feat) { feats($word) =~ /$feat=(\w+)/; return $1 // ""; }
sub get_feats($word, @feats) { return map { get_feat($word, $_) } @feats; }

1;
