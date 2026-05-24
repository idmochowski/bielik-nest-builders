/* ═══════════════════════════════════════════════
   Agent Architectures — Speaker Notes (Polish)
   Press S during presentation to toggle notes
   ═══════════════════════════════════════════════ */

const SPEAKER_NOTES = {
  0: {
    time: '~1 min',
    text: 'Tytulowa strona. Przedstaw sie, powiedz o czym bedzie prezentacja.',
    points: [
      'Przedstaw: imie, rola, zwiazek z projektem Bielik',
      'Krotko: dzisiaj omowimy 7 architektur agentow AI — od ReAct po Multi-Agent',
      'Wszystkie przyklady w kontekscie NAT (NVIDIA NeMo Agent Toolkit) + Bielik-Minitron-7B',
      'Materialy: docs/agent-types.md ma pelna dokumentacje'
    ]
  },
  1: {
    time: '~3 min',
    text: 'Wprowadzenie — co to jest architektura agenta i dlaczego ma znaczenie.',
    points: [
      'Zacznij od pytania: "Kto z was budowal agenta AI? Jakie problemy mieliscie?"',
      'Architektura = wzorzec organizacji interakcji LLM-narzedzia',
      'Pokaz spectrum — od prostego (Tool Calling, 1 krok) do zlozonego (LATS, drzewo)',
      'Nacisknij: nie ma "najlepszej" architektury, jest odpowiednia do zadania',
      'Klikniecie na spectrum przenosi do odpowiedniego slidu'
    ]
  },
  2: {
    time: '~5 min',
    text: 'ReAct — glowna architektura uzywana na warsztatach.',
    points: [
      'Kluczowe: Thought → Action → Observation w petli',
      'Pokaz diagram krok po kroku (fragmenty)',
      'Zaznacz: transparentnosc — widac kazdy krok rozumowania',
      'Dlaczego ReAct dla Bielik 7B? Nie wymaga natywnego tool calling',
      'TO MY UZYWAMY — cwiczenia 1-4 w Part 2 oparte na ReAct',
      'Slabosc: moze sie zapetlic, dlatego max_tool_calls w config.yaml'
    ]
  },
  3: {
    time: '~3 min',
    text: 'Tool Calling Agent — natywne API do wywolywania funkcji.',
    points: [
      'Roznica vs ReAct: strukturalny JSON zamiast parsowania tekstu',
      'Vantaggio: bardziej niezawodny, szybszy',
      'Wymaganie: vLLM z --enable-auto-tool-choice + custom parser',
      'Dla Bielik 7B: mozliwe ale wymaga odpowiedniej konfiguracji serwera',
      'Jako ulepszenie ReAct gdy serwer wspiera tool calling'
    ]
  },
  4: {
    time: '~4 min',
    text: 'ReWOO — planowanie upfront, potem rownolegle wykonanie.',
    points: [
      'Klucz: 3 fazy — Planner → Worker (rownolegle) → Solver',
      'Pokaz jak narzedzia moga dzialac jednoczesnie',
      'Tylko 2-3 wywolania LLM vs N w ReAct — duza oszczednosc',
      'Idealny do: "porownaj X i Y" — kroki przewidywalne i niezalezne',
      'Nie nadaje sie: eksploracja, gdzie nastepny krok zalezy od poprzedniego'
    ]
  },
  5: {
    time: '~4 min',
    text: 'Plan-and-Execute — dekompozycja na podzadania.',
    points: [
      'Dwie role: Planner (strateg) i Executor (wykonawca)',
      'Planner MOZE poprawiac plan po kazdym kroku — kluczowa roznica vs ReWOO',
      'Cwiczenie 4: ReAct orchestrator = prosty Plan-and-Execute',
      'Dobry do zlozonych zadan: research → analiza → raport',
      'Koszt: 2 LLM per cykl (planner + executor)'
    ]
  },
  6: {
    time: '~3 min',
    text: 'Reflexion — samokrytyka i iteracyjne poprawki.',
    points: [
      'Klucz: Agent dziala → Evaluator ocenia → Agent poprawia',
      'Pokaz "quality meter" — jakosc rosnie z kazda runda',
      'Dobre dla: raporty, kod, analiza — gdzie jakosc > szybkoosc',
      'Nie dla: real-time chat (za wolny, 2x wywolan na runde)',
      'Ciekawostka: evaluator moze byc tym samym LLM z innym promptem'
    ]
  },
  7: {
    time: '~3 min',
    text: 'LATS — tree search dla zlozonego reasoningu.',
    points: [
      'Inspeiracja: Monte Carlo Tree Search z LLM jako heurystyka',
      'Eksploruje wiele sciezek, cofa sie z slepych zauilkow',
      'Bardzo drogi: N x gałęzie wywolan LLM',
      'Dobry dla: matematyka, logika, planowanie',
      'Overkill dla: information retrieval, proste queries',
      'Rzadko uzywany w produkcji — glownie badania'
    ]
  },
  8: {
    time: '~4 min',
    text: 'Multi-Agent — wzorce orkiestracji wielu agentow.',
    points: [
      '4 wzorce: Router, Pipeline, Parallel, Hierarchical',
      'Router = Cwiczenie 4: Bielik jako orchestrator, research_agent + writing_crew',
      'Pipeline: liniowy, przewidywalny, latwy do debugowania',
      'Parallel: szybki dla niezaleznych podzadan',
      'Hierarchical: duze systemy, wiele poziomow delegacji',
      'NAT YAML composition umozliwia wszystkie te wzorce'
    ]
  },
  9: {
    time: '~3 min',
    text: 'Porownanie — tabela decyzyjna.',
    points: [
      'Pokaz wiersz po wierszu (fragmenty)',
      'Zielony = zaleta/low cost, czerwony = koszt/wymaganie',
      'Zwróc uwage na: ReWOO (najtanszy) vs LATS (najdrozsszy)',
      'Pytanie do publicznosci: "Ktory wzorzec wybralibyscie do X?"',
      'Klucz: nie ma uniwersalnego — zalezy od zadania, modelu, budzetu'
    ]
  },
  10: {
    time: '~3 min',
    text: 'Podsumowanie — kluczowe wnioski i odnosniki.',
    points: [
      'Kazda karta = jeden wymiar decyzyjny',
      'Nasz wybor: ReAct — niezawodny z Bielik 7B, transparentny do nauki',
      'Wskaz dokumentacje: docs/agent-types.md',
      'Wskaz nastepny krok: cwiczenia w Part 2',
      'Podziekuj, zachec do pytan'
    ]
  }
};
