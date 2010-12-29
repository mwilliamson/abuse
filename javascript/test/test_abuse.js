AbuseTest = TestCase("AbuseTest");

(function() {
    var parse = ZWOBBLE.abuse.parse;
    var generate = ZWOBBLE.abuse.generate;
    var generateAll = ZWOBBLE.abuse.generateAll;
    var terminal = ZWOBBLE.abuse.terminal;
    var nonTerminal = ZWOBBLE.abuse.nonTerminal;
    
    var assertNonTerminal = function(actual, name) {
        assertTrue(actual.isNonTerminal);
        assertEquals(name, actual.name);
    };
    
    var assertTerminal = function(actual, text) {
        assertTrue(actual.isTerminal);
        assertEquals(text, actual.text);
    };
    
    var assertRule = function(actual, nonTerminalName, right) {
        var i;
        assertNonTerminal(actual.left, nonTerminalName);
        assertEquals(right.length, actual.right.length);
        for (i = 0; i < right.length; i += 1) {
            if (right[i].isTerminal) {
                assertTerminal(actual.right[i], right[i].text);
            } else {
                assertNonTerminal(actual.right[i], right[i].name);
            }
        }
    };

    // Parsing
    
    AbuseTest.prototype.testCanParseSourceWithOnlyWhitespace = function() {
        var rules = parse("\n\n\n\n\n\r\t\t \n\n     \r\n\n").rules;
        assertEquals(0, rules.length);
    };
    
    AbuseTest.prototype.testCanReadRuleForTerminalToNonTerminal = function() {
        var rules = parse("$SENTENCE -> I hate you!").rules;
        assertEquals(1, rules.length);
        assertRule(rules[0], "SENTENCE", [terminal("I hate you!")]);
    };

    AbuseTest.prototype.testCanReadMultipleRulesSeparatedByNewLines = function() {
        var rules = parse("$SENTENCE -> I hate you!\n$SENTENCE -> You smell!").rules;
        assertEquals(2, rules.length);
        assertRule(rules[0], "SENTENCE", [terminal("I hate you!")]);
        assertRule(rules[1], "SENTENCE", [terminal("You smell!")]);
    };

    AbuseTest.prototype.testWhitespaceIsTrimmedFromRight = function() {
        var rules = parse("$SENTENCE -> I hate you!   \t\t  ").rules;
        assertEquals(1, rules.length);
        assertRule(rules[0], "SENTENCE", [terminal("I hate you!")]);
    };
    
    AbuseTest.prototype.testFinalTerminalIsOnlyTrimmedOnTheRight = function() {
        var rules = parse("$VERY -> $VERY very").rules;
        assertRule(rules[0], "VERY", [nonTerminal("VERY"), terminal(" very")]);
    };
    
    AbuseTest.prototype.testEmptyTerminalsAreNotProducedByRules = function() {
        var rules = parse("$SENTENCE -> $INSULT").rules;
        assertRule(rules[0], "SENTENCE", [nonTerminal("INSULT")]);
    };

    AbuseTest.prototype.testIgnoresBlankLines = function() {
        var rules = parse("\n    \t\n\n$SENTENCE -> I hate you!\n     \n\n$SENTENCE -> You smell!\n\n\n").rules;
        assertEquals(2, rules.length);
        assertRule(rules[0], "SENTENCE", [terminal("I hate you!")]);
        assertRule(rules[1], "SENTENCE", [terminal("You smell!")]);
    };
    
    AbuseTest.prototype.testCanReadNonTerminalsOnRight = function() {
        var rules = parse("$SENTENCE -> You're as $ADJ as a $ANIMAL").rules;
        assertEquals(1, rules.length);
        assertRule(rules[0], "SENTENCE",
                   [terminal("You're as "), nonTerminal("ADJ"),
                    terminal(" as a "), nonTerminal("ANIMAL")]);
    };
    
    AbuseTest.prototype.testNonTerminalsAreAlphanumericAndUnderscoresOnly = function() {
        var rules = parse("$SENTENCE -> You smell of $Smell2.").rules;
        assertEquals(1, rules.length);
        assertRule(rules[0], "SENTENCE", [terminal("You smell of "), nonTerminal("Smell2"), terminal(".")]);
    };
    
    AbuseTest.prototype.testCanUseBracesToIndicateNonTerminals = function() {
        var rules = parse("$SENTENCE -> You're ${RUDE_ADJ}er than I thought").rules;
        assertEquals(1, rules.length);
        assertRule(rules[0], "SENTENCE", [terminal("You're "), nonTerminal("RUDE_ADJ"), terminal("er than I thought")]);
    };
    
    AbuseTest.prototype.testAddsErrorWithLineNumberIfArrowIsMissing = function() {
        var errors = parse("\n\n$SENTENCE - You're ${RUDE_ADJ}er than I thought\n" +
                           "$RUDE_ADJ ->\n" +
                           "$SENTENCE -> $RUDE_ADJ").errors;
        assertEquals(1, errors.length);
        assertEquals("Missing symbol on line 3: ->", errors[0].str);
        assertEquals(ZWOBBLE.abuse.errors.missingArrow, errors[0].type);
        assertEquals(3, errors[0].lineNumber);
    };
    
    AbuseTest.prototype.testAddsErrorWithLineNumberIfClosingBraceIsMissing = function() {
        var errors = parse("\n\n$SENTENCE -> You're ${RUDE_ADJer than I thought\n" +
                           "$SENTENCE ->\n").errors;
        assertEquals(1, errors.length);
        assertEquals("Missing closing brace on line 3 (opening brace at character 22)", errors[0].str);
        assertEquals(ZWOBBLE.abuse.errors.missingClosingBrace, errors[0].type);
        assertEquals(3, errors[0].lineNumber);
        assertEquals(22, errors[0].openingBraceCharacterNumber);
    };
    
    AbuseTest.prototype.testAddsErrorWithLineNumberIfClosingBraceForSecondVariableIsMissing = function() {
        var errors = parse("\n\n$SENTENCE -> You're ${RUDE_ADJ}er than ${OBJ\n" +
                           "$SENTENCE ->\n\n").errors;
        assertEquals(1, errors.length);
        assertEquals("Missing closing brace on line 3 (opening brace at character 41)", errors[0].str);
    };
    
    AbuseTest.prototype.testAddsErrorIfNonTerminalIsUsedWithNoMatchingProductionRule = function() {
        var errors = parse("\n\n$SENTENCE -> $INSULT\n\n").errors;
        assertEquals(1, errors.length);
        assertEquals("No production rule for non-terminal $INSULT (line 3, character 14)", errors[0].str);
        assertEquals(ZWOBBLE.abuse.errors.noProductionRule, errors[0].type);
        assertEquals("INSULT", errors[0].nonTerminal);
        assertEquals(3, errors[0].lineNumber);
        assertEquals(14, errors[0].characterNumber);
    };
    
    AbuseTest.prototype.testAddsErrorIfSentenceHasNoProductionRule = function() {
        var errors = parse("").errors;
        assertEquals(1, errors.length);
        assertEquals("No production rule for non-terminal $SENTENCE", errors[0].str);
        assertEquals(ZWOBBLE.abuse.errors.noProductionRule, errors[0].type);
        assertEquals("SENTENCE", errors[0].nonTerminal);
    };
    
    AbuseTest.prototype.testAddsErrorIfProductionRuleIsNeverUsed = function() {
        var errors = parse("$SENTENCE -> \n$RUDE_ADJ -> ugly").errors;
        assertEquals(1, errors.length);
        assertEquals("Production rule with start symbol $RUDE_ADJ is never used (line 2)", errors[0].str);
        assertEquals(ZWOBBLE.abuse.errors.ruleNeverUsed, errors[0].type);
        assertEquals(2, errors[0].lineNumber);
    };
    
    // Generation
    
    var staticSelector = function(choices) {
        return function(length) {
            return choices.shift();
        };
    };
    
    AbuseTest.prototype.testCanGenerateSentenceFromSimpleRule = function() {
        var rules = parse("$SENTENCE -> I hate you!").rules; 
        assertEquals("I hate you!", generate(rules, staticSelector([0])));
    };
    
    AbuseTest.prototype.testUsesSelectorToPickRuleWhenThereAreManyPossibleRules = function() {
        var rules = parse("$SENTENCE -> I hate you!\n$SENTENCE -> Go away!").rules; 
        assertEquals("I hate you!", generate(rules, staticSelector([0])));
        assertEquals("Go away!", generate(rules, staticSelector([1])));
    };
    
    AbuseTest.prototype.testCanUseIntermediateRules = function() {
        var rules = parse("$SENTENCE -> You smell of $SMELL\n" +
                          "$SMELL -> elderberries\n" +
                          "$SMELL -> dogfood").rules; 
        assertEquals("You smell of elderberries", generate(rules, staticSelector([0, 0])));
        assertEquals("You smell of dogfood", generate(rules, staticSelector([0, 1])));
    };
    
    AbuseTest.prototype.testSentenceGenerationResortsToPickingSentenceRandomlyFromAllSentencesIfMaximumDepthIsReached = function() {
        var rules = parse("$SENTENCE -> B\n" + 
                          "$SENTENCE -> A $SENTENCE").rules;
        assertEquals("A A B", generate(rules, staticSelector([1, 1, 1, 2]), 3));
    };
    
    AbuseTest.prototype.testSentenceGenerationResortsToPickingSentenceRandomlyFromAllSentencesIfNonTerminalCannotBeExpanded = function() {
        var rules = parse("$SENTENCE -> $RUDE_WORD\n" + 
                          "$SENTENCE -> Go away!").rules;
        assertEquals("Go away!", generate(rules, staticSelector([0, 0])));
    };
    
    AbuseTest.prototype.testCanGenerateEmptySentence = function() {
        var rules = parse("$SENTENCE -> ").rules;
        assertEquals("", generate(rules, staticSelector([0])));
    };
    
    AbuseTest.prototype.testCanGenerateAllSentences = function() {
        var rules = parse("$SENTENCE -> I hate you!\n" + 
                          "$SENTENCE -> You smell of $SMELL\n" +
                          "$SMELL -> elderberries\n" +
                          "$SMELL -> dogfood\n" +
                          "$SENTENCE -> You're as $RUDE_ADJ as my $PET\n" +
                          "$RUDE_ADJ -> ugly\n" +
                          "$RUDE_ADJ -> stupid\n" +
                          "$PET -> rat\n" +
                          "$PET -> dog\n").rules;
        var results = generateAll(rules);
        assertEquals(7, results.length);
        assertEquals("I hate you!", results[0]);
        assertEquals("You smell of elderberries", results[1]);
        assertEquals("You smell of dogfood", results[2]);
        assertEquals("You're as ugly as my rat", results[3]);
        assertEquals("You're as ugly as my dog", results[4]);
        assertEquals("You're as stupid as my rat", results[5]);
        assertEquals("You're as stupid as my dog", results[6]);
    };
    
    AbuseTest.prototype.testSettingDepthOnGenerateAllLimitsRecursionDepth = function() {
        var rules = parse("$SENTENCE -> B\n" + 
                          "$SENTENCE -> A $SENTENCE").rules;
        var results = generateAll(rules, 3);
        
        assertEquals("B", results[0]);
        assertEquals("A B", results[1]);
        assertEquals("A A B", results[2]);
        assertEquals(3, results.length);
    };
    
    AbuseTest.prototype.testEmptyRuleSetGeneratesNoSentences = function() {
        var rules = parse("").rules;
        var results = generateAll(rules);
        assertEquals(0, results.length);
    };
})();
