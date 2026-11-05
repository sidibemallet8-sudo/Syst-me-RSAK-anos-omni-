
from anos_omni_rsak import AnosOmniRSAK
import json


def main():
    ai = AnosOmniRSAK()

    print("=" * 50)
    print("       ANOS OMNI — RSAK V1")
    print("       LABORATOIRE EXPERIMENTAL")
    print("=" * 50)

    print("\n[1] Création d'une règle initiale")

    rule_id = ai.add_rule(
        {"wheels": 4},
        "motorized"
    )

    print("Règle créée :", rule_id)

    print("\n[2] Apprentissage d'un exemple positif")

    ai.add_example(
        {"wheels": 4, "engine": True},
        "motorized"
    )

    print("Exemple mémorisé.")

    print("\n[3] Présentation d'un contre-exemple")

    conflicts = ai.add_example(
        {"wheels": 4, "engine": False},
        "not_motorized"
    )

    print("Contradictions détectées :", conflicts)

    print("\n[4] Proposition de réorganisation")

    proposal = ai.propose_reorganization(rule_id)

    if proposal is None:
        print("Aucune réorganisation proposée.")
        return

    print(json.dumps(proposal, indent=2))

    print("\n[5] Validation humaine simulée")

    ai.validate(proposal["id"], True)

    print("Réorganisation acceptée dans ce scénario de démonstration.")

    print("\n[6] Nouvelle interrogation")

    result = ai.query({
        "wheels": 4,
        "engine": False
    })

    print(json.dumps(result, indent=2))

    print("\n[7] Sauvegarde de la mémoire")

    ai.save("anos_memory.json")

    print("Mémoire sauvegardée.")

    print("\nDÉMONSTRATION TERMINÉE")


if __name__ == "__main__":
    main()
