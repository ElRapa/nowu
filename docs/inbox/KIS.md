## failing is a valid outcome (keywords: flow, artifacts; 2026-03-10) ***
When we are working on a task or trying to solve a problem, it's important to recognize that failure is a valid outcome. Not every attempt will be successful, and that's okay. In fact,
sometimes we just need to know that something can't be done in the way we intended or at all. So instead of trying to force a solution, we should capture the failure mode and the reason why it failed. This is valuable information for future iterations and for understanding the limitations of our current approach.

## add status of last session to session-state (keywords: flow, memory; 2026-03-10) **
use session state to keep track of our progress and intentions. add status of last sessions and todos. So we know if we finished our intended task or if we failed. This way we know how to continue or if we finished everything and can do the next task. 

## requirements scope sensitive  (keywords: requirements, scope; 2026-03-11) **
When we are working on requirements, it's important to consider the scope of each requirement.
Some requirements are "global", others are just for a function. Make the requirements management smart so that global ones are always in scope and more granular requirements only relevant for the relevant functions. This way we can keep the requirements list clean and focused, while still ensuring that all necessary requirements are considered when working on a specific task.

## requirements inheritance (keywords: requirements, hierarchy; 2026-03-11) **
When we have a hierarchy of functions or modules, it would be useful if the requirements could be inherited down the hierarchy. For example, if a module has a requirement, all functions within that module should also be aware of that requirement. This way we can ensure that all relevant requirements are considered at every level of the project, without having to duplicate them for each function or module. Also some requirements are more specific versions of more general requirements. For example, a general requirement might be "the system should be secure", while a more specific requirement might be "the system should use encryption for all data in transit". The specific requirement should be linked to the general requirement, so that we can see the relationship between them and ensure that all relevant requirements are considered when working on a specific task.

## place requirements in the CPG-Pyramid or in the C4-Model (or equivalent) (keywords: requirements, architecture; 2026-03-11) ****
When we are working on defining requirements we should place them in the appropriate level of the architecture. For example, high-level requirements that apply to the entire system should be placed at the top of the CPG-Pyramid or in the context diagram of the C4-Model. More specific requirements that apply to a particular module or function should be placed at the appropriate level in the hierarchy. This way we can ensure that all requirements are organized and easily accessible, and that we can see how they relate to the overall architecture of the system.

## add level of decision
some decisions are made on the system level, others on the code level, others are product level. Track the level to allow filtering and later better connecting of decision to impact/implemenation

## Diamond on pyramid model
the final artifact could be seen as a diamond stacked on a pyramid. The peak is the vision, which widens to use cases, feature-ideas and on the widest level; requirements, they narrow down to decisions or cluster of architectural requirements, and these can be projected on the pyramid, where "clusters architectural requirements and decisions" are connected to the system level and the fine granular requirements on the widest diamond layer map to the code implementation. (The pyramid is the cpg and the dimaond is some kind of product defining model)