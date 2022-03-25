import { automaton } from "./automaton";
import { unit } from "./unit";

export interface production {
    id: number,
    id_unit: number,
    unit: unit,
    id_automaton: number,
    automaton: automaton,
    tankTemperature: number,
    outsideTemperature: number,
    milkWeight: number,
    finalizedProductWeight: number,
    ph: number,
    k: number,
    naci: number,
    salmonel: number,
    ecoli: number,
    listeria: number,
    generatedTime: Date,
}