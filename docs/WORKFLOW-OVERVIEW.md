```mermaid
flowchart LR
  %% STYLE HINTS
  classDef agentStep fill=#e0f7fa,stroke=#006064,color=#000,stroke-width=1px;
  classDef humanGate fill=#ffe0b2,stroke=#e65100,color=#000,stroke-width=1px;
  classDef artifact fill=#e8eaf6,stroke=#1a237e,color=#000,stroke-width=1px;
  classDef loopEdge stroke-dasharray: 5 5;

  %% PRE-WORKFLOW P-1..P4
  subgraph PRE["Pre-Workflow (P0–P4)"]
    direction LR

    Pm[\"P-1 Mode Selection\n(size, stage, mode)\"]
    class Pm agentStep

    subgraph P0["P0 Signal Capture"]
      direction TB
      P0V[\"P0.V Vision Bootstrap\n(agent → docs/vision.md DRAFT)\"]
      P01[\"P0.1 Idea Note\n(human → idea-NNN.md)\"]
      P0D[\"P0.D Idea Decomposition\n(agent → NNN-decomp.md + mode)\"]
      P02[\"P0.2 Vision Alignment Check\n(human gate)\"]
      class P0V,P0D agentStep
      class P01,P02 humanGate
    end

    subgraph P1["P1 Discovery"]
      direction TB
      P11[\"P1.1 Research\n(discovery agent → disc-NNN-research.md)\"]
      P12[\"P1.2 Perspective Interview\n(agent → problem-NNN.md DRAFT)\"]
      P13[\"P1.3 Problem Statement Gate\n(human → problem-NNN APPROVED)\"]
      class P11,P12 agentStep
      class P13 humanGate
    end

    subgraph P2["P2 Story Mapping"]
      direction TB
      P21[\"P2.1 Epic + Story Draft\n(agent → epic-NNN.md + story-NNN-*.md)\"]
      P22[\"P2.2 Story Review Gate\n(human → stories APPROVED)\"]
      class P21 agentStep
      class P22 humanGate
    end

    subgraph P3["P3 Architecture Bootstrap"]
      direction TB
      P31[\"P3.1 Constraint Check\n(agent → NNN-constraint-check.md)\"]
      P32[\"P3.2 Architecture Bootstrap\n(agent → arch-pass-NNN.md)\"]
      P33[\"P3.3 ADR Creation\n(human → ADR-NNN-*.md)\"]
      class P31,P32 agentStep
      class P33 humanGate
    end

    subgraph P4["P4 Readiness Assembly"]
      direction TB
      P41[\"P4.1 Readiness Check\n(agent → NNN-readiness.md)\"]
      P42[\"P4.2 Intake Brief Assembly\n(agent → intake-NNN.md DRAFT)\"]
      P43[\"P4.3 Human Final Approval\n(human → intake-NNN READY_FOR_S1)\"]
      class P41,P42 agentStep
      class P43 humanGate
    end
  end

  %% DELIVERY LOOP S1..S9
  subgraph S["Delivery Loop (S1–S9)"]
    direction LR

    S1[\"S1 Intake\n(check intake-NNN)\"]
    S2[\"S2 Architecture Analysis\n(constraints sheet)\"]
    S3[\"S3 Design Options\n(options sheet)\"]
    S4[\"S4 Decision 🛑\n(human validation gate)\"]
    S5[\"S5 Shaping 🛑\n(human validation gate)\"]
    S6[\"S6 Implementation\n(code + tests)\"]
    S7[\"S7 VBR\n(auto checks)\"]
    S8[\"S8 Review 🛑\n(human-like review)\"]
    S9[\"S9 Capture 🛑\n(progress + next_cycle_trigger)\"]
    class S1,S2,S3,S6,S7 agentStep
    class S4,S5,S8,S9 humanGate
  end

  %% MAIN PRE-WORKFLOW FLOW
  Pm --> P0V
  P0V --> P01
  P01 --> P0D
  P0D --> P02

  %% Mode-based entry into P1/P2/P3
  P02 -->|Lite / Standard / Full / Bootstrap| P11
  P11 --> P12 --> P13 --> P21 --> P22

  %% P3 only for Full / Bootstrap (conceptual)
  P22 -->|Lite / Standard| P41
  P22 -->|Full / Bootstrap| P31
  P31 --> P32 --> P33 --> P41

  %% Readiness to intake
  P41 --> P42 --> P43
  P43 -->|state/intake/intake-NNN READY_FOR_S1| S1

  %% DELIVERY MAIN LINE
  S1 --> S2 --> S3 --> S4 --> S5 --> S6 --> S7 --> S8 --> S9

  %% FEEDBACK LOOPS FROM S9
  S9 -->|"next_cycle_trigger = CONTINUE\n(next story, same epic)"| P21
  S9 -->|"ARCH_PIVOT\n(re-check architecture)"| P31
  S9 -->|"PRODUCT_PIVOT\n(new discovery)"| P11
  S9 -->|"COMPLETE\n(epic / product goal met)"| End[(Cycle complete)]

  %% OPTIONAL: HEALTH CHECK ENTRYPOINTS
  HAll[\"/health-check all\n(vision, architecture, goals)\"]:::artifact
  HAll -->|"findings\n→ choose entry"| Pm

  %% OPTIONAL: GAP (Global Architecture Pass)
  GAP[\"Global Architecture Pass (GAP)\nupdate global C4 L1/L2 + ADRs\"]:::agentStep
  GAP -->|"constraints for per-epic P3"| P31
```

