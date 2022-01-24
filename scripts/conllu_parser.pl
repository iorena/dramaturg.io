#!/usr/bin/perl
use warnings;
use strict;
use v5.20;
use utf8;
no warnings "experimental::signatures";
use feature qw(postderef signatures);

my (@sentences, @conllu_field_names, @nsubj_verb_obj_triplets);
my (%word_counts, %skip_pos, %skip_deprel);

@conllu_field_names = ("ID", "FORM", "LEMMA", "UPOS", "XPOS", "FEATS", "HEAD", "DEPREL", "DEPS", "MISC");

#@skip_pos{qw(ADP ADV CCONJ PUNCT SCONJ)} = ();
#@skip_deprel{qw(nmod appos nummod amod)} = ();

sub baseform($x) { return $x =~ s/:.*//r; }
sub bad_deprel($deprel) { return exists $skip_deprel{baseform($deprel)}; }
sub bad_pos($upos) { return exists $skip_pos{$upos}; }

sub id($word) { return $word->{'ID'}; }
sub form($word) { return $word->{'FORM'}; }
sub lemma($word) { return $word->{'LEMMA'}; }
sub feats($word) { return $word->{'FEATS'}; }
sub head($word) { return $word->{'HEAD'}; }
sub upos($word) { return $word->{'UPOS'}; }
sub deprel($word) { return $word->{'DEPREL'}; }

sub is_verb($word) { return upos($word) eq "VERB"; }
sub is_noun($word) { return upos($word) eq "NOUN"; }
sub is_pron($word) { return upos($word) eq "PRON"; }
sub is_propn($word) { return upos($word) eq "PROPN"; }
sub is_aux($word) { return upos($word) eq "AUX"; }

sub is_nsubj($word) { return baseform(deprel($word)) eq "nsubj" };
sub is_obj($word) { return deprel($word) eq "obj" };
#sub is_obl($word) { return deprel($word) eq "obl" };
#sub is_nsubj_cop($word) { return deprel($word) eq "nsubj:cop" };
#sub is_cop($word) { return deprel($word) eq "cop" };
sub is_xcomp($word) { return baseform(deprel($word)) eq "xcomp"; }
sub is_compound($word) { return baseform(deprel($word)) eq "compound"; }
sub is_clause_modifier($word) { my $bf = baseform(deprel($word)); return $bf eq "acl" || $bf eq "advcl"; }

sub count($word) { return $word_counts{lemma($word)}; }

sub case($feats) { $feats =~ /Case=(\w+)/; return $1 // ""; }
#sub number($feats) { $feats =~ /Number=(\w+)/; return $1 // ""; }

sub is_compound_word($lemma) { return index($lemma, "#") != -1; }
sub add_compound_word_counts() {
    for my $lemma (keys %word_counts) {
        next unless is_compound_word($lemma);
        $word_counts{$_} += $word_counts{$lemma} for split("#", $lemma);
    }
}

sub word($id, $form, $lemma, $upos, $feats, $head, $deprel) {
    return {
        'ID' => $id,
        'FORM' => $form,
        'LEMMA' => $lemma,
        'UPOS' => $upos,
        'FEATS' => case($feats), # . number($feats),
        'HEAD' => $head,
        'DEPREL' => $deprel
    };
}

sub new_sentence($text) {
    push @sentences, {
        'text' => $text,
        'words' => [],
        'score' => 0
    };
    return $sentences[$#sentences];
}

sub score_word($word) {
    if (is_compound_word(lemma($word))) {
        my @parts = split("#", lemma($word));
        my $score = 0;
        $score += $word_counts{$_} for (@parts);
        return $score / @parts;
    }
    return count($word);
}

sub score_sentences() {
    for my $sentence (@sentences) {
        my ($n, $score) = (0) x 2;
        for my $word ($sentence->{'words'}->@*) {
            next unless is_noun($word) || is_propn($word);
            $score += score_word($word);
            ++$n;
        }
        $sentence->{'score'} = $score / $n if $n > 0;
    }
}

sub make_graph($sentence) {
    my %graph;
    my @words = $sentence->{'words'}->@*;
    $graph{id($_)} = { 'word' => $_, 'adj' => [], 'radj' => [] } for @words;
    for my $word (@words) {
        my ($id, $head) = (id($word), head($word));
        next unless exists $graph{$head};
        push $graph{$head}->{'adj'}->@*, $word;
        push $graph{$head}->{'radj'}->@*, $graph{$id}->{'word'};
        
    }
    return %graph;
}

sub head_form($graph, $head) {
    my $head_word = $graph->{$head}->{'word'};
    my $str = lemma($head_word);
    # Find related verb.
    $str = lemma($graph->{head($head_word)}->{'word'}) . " " . $str if head($head_word) != 0 && is_xcomp($head_word) && is_verb($graph->{head($head_word)}->{'word'});
    my @aux;
    for ($graph->{$head}->{'radj'}->@*) {
        push @aux, $_ if is_aux($_);
    }
    $str = lemma($_) . " " . $str for sort { -id($a) <=> -id($b) } @aux;
    return $str;
}

sub nsubj_form($graph, $id) {
    my $nsubj_word = $graph->{$id}->{'word'};
    my $str = form($nsubj_word);
    my (@after, @before);
    for ($graph->{$id}->{'radj'}->@*) {
        push @after, $_ if baseform(deprel($_)) eq "flat";
        push @before, $_ if index(deprel($_), "mod") != -1;
    }
    $str = form($_) . " " . $str for sort { -id($a) <=> -id($b) } @before;
    $str .= " " . form($_) for sort { -id($a) <=> -id($b) } @after;
    return $str;
}

sub obj_form($graph, $id) {
    my $obj_word = $graph->{$id}->{'word'};
    my $str = lemma($obj_word);
    for ($graph->{head($obj_word)}->{'adj'}->@*) {
        next unless is_xcomp($_);
        $str .= " " . lemma($_);
    }
    return $str;
}

sub print_sentence($sentence) {
    printf "%s\n%s\nScore: %.3f\n\n", "-" x 100, $sentence->{'text'}, $sentence->{'score'};
    for my $fn (@conllu_field_names[(0, 1, 2, 3, 5, 6, 7)]) {
        printf("%-6s\t", $fn);
        printf("%-14s\t", substr($_->{$fn}, 0, 14)) for $sentence->{'words'}->@*;
        say "";
    }
    say "";
}

sub new_triplet($sentence, $triplet_score, $nsubj, $verb, $obj, $verb_deprel, $obj_feats) {
    return {
        'sentence' => $sentence,
        'score' => $triplet_score,
        'nsubj' => $nsubj,
        'verb' => $verb,
        'obj' => $obj,
        'verb_deprel' => $verb_deprel,
        'obj_feats' => $obj_feats
    };
};

sub print_triplet($triplet) {
    #print_sentence($triplet->{'sentence'});
    printf "\"%s\",\"%s\",\"%s\",\"%s\"\n", $triplet->{'nsubj'}, $triplet->{'verb'}, $triplet->{'obj'}, $triplet->{'obj_feats'};
}

sub find_nsubj_verb_obj_triplet($sentence) {
    my %graph = make_graph($sentence);
    for my $head (keys %graph) {
        my $head_word = $graph{$head}->{'word'};
        next unless is_verb($head_word);

        # Skip clausal modifiers.
        next if is_clause_modifier($head_word);
        next if head($head_word) != 0 && is_verb($graph{head($head_word)}->{'word'}) && is_clause_modifier($graph{head($head_word)}->{'word'});

        # Related words for verb.
        my $head_word_form = head_form(\%graph, $head);

        my @adj = $graph{$head}->{'adj'}->@*;
        for my $i (0..$#adj) {
            my $nsubj_word = $adj[$i];
            next unless is_nsubj($nsubj_word) && !is_pron($nsubj_word);

            # Related words for nsubj.
            my $nsubj_word_form = nsubj_form(\%graph, id($nsubj_word));

            for my $j (0..$#adj) {
                next if $i == $j;
                my $obj_word = $adj[$j];
                next unless is_obj($obj_word);

                # Related words for obj.
                my $obj_word_form = obj_form(\%graph, id($obj_word));

                my $triplet_score = (score_word($nsubj_word) + score_word($obj_word) + score_word($head_word)) / 3;
                push @nsubj_verb_obj_triplets, new_triplet($sentence, $triplet_score, $nsubj_word_form, $head_word_form, $obj_word_form, deprel($head_word), feats($obj_word));
            }
        }
    }
}

# Read all sentences by parsing CoNLL-U formated standard input.
while (<>) {
    chomp;
    next unless /^# text = (.*)/;
    my $sentence = new_sentence($1);
    while (<>) {
        last if /^#/ || !/\S/;
        my ($id, $form, $lemma, $upos, undef, $feats, $head, $deprel) = split /\t/;
        next if bad_pos($upos) || bad_deprel($deprel);
        ++$word_counts{$lemma};
        push $sentence->{'words'}->@*, word($id, $form, $lemma, $upos, $feats, $head, $deprel);
    }
}

add_compound_word_counts();
score_sentences();
find_nsubj_verb_obj_triplet($_) for @sentences;

#say $_, "=", $word_counts{$_} for sort { $word_counts{$a} <=> $word_counts{$b} } keys %word_counts;
#print_sentence($_) for sort { $a->{'score'} <=> $b->{'score'} } @sentences;
print_triplet($_) for sort { -$a->{'score'} <=> -$b->{'score'} || -$a->{'sentence'}->{'score'} <=> -$b->{'sentence'}->{'score'} } @nsubj_verb_obj_triplets;
