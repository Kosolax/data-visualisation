import { Component, OnInit } from '@angular/core';
import { production } from '../object/production';
import { ProductionService } from '../services/production.service';
import { unit } from '../object/unit';
import { automaton } from '../object/automaton';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  list: production[] = [];
  units: unit[] = [];
  automatons: automaton[] = [];
  productionService: ProductionService;

  currentUnit : number = 1;
  currentAutomaton : number = 1;
  currentCharts : string = 'tankTemperature';

  PropretyList : string[] = [
    'tankTemperature',
    'outsideTemperature',
    'milkWeight',
    'finalizedProductWeight',
    'ph',
    'k',
    'naci',
    'salmonel',
    'ecoli',
    'listeria',]

  public graph = {
    data: [
        { x: ["1"], y: [1], type: 'scatter', mode: 'lines+points', marker: {color: 'red'} },
    ],
    layout: {title: 'Aucune donnéees', x: [1]},
    config: {responsive: true}
  };

  constructor(productionService: ProductionService) {
    this.productionService = productionService;
  }

  ngOnInit(): void {
    this.productionService.getConfig()
    .subscribe(
      {
        next: value =>
        {
          this.units = value as unit[];
          this.generateChart();
        }
      }
    );
  }

  requestAutomatons(inutNumber : number): void {
    this.currentUnit = inutNumber;
    this.productionService.getRequestAutomate(inutNumber)
    .subscribe(
      {
        next: value =>
        {
          this.automatons = value as automaton[];
          this.generateChart();
        }
      }
    );
  }

  requestCharts(chart : string): void {
    this.currentCharts = chart;
    
  }

  request(automateNumber : number): void {
    this.currentAutomaton = automateNumber;
    this.productionService.getRequest(this.currentUnit, automateNumber)
    .subscribe(
      {
        next: value =>
        {
          this.list = value as production[];
        }
      }
    );
  }

  changeChart(ChartName : string): void {
    this.currentCharts = ChartName;
    this.generateChart();
  }

  generateChart(): void {
    if (this.list.length > 0) {

      var timeList: string[] = []
      var tempList: number[] = []
      this.list.forEach(x => { 
        timeList.push(x.generatedTime.toLocaleString());
      })

      switch (this.currentCharts) {
        case 'tankTemperature':

          this.list.forEach(x => tempList.push(x.tankTemperature));

          this.graph = {
            data: [
              { x: timeList, y: tempList, type: 'scatter', mode: 'lines+points', marker: {color: 'red'} },
            ],
            layout: {title: "La température de la cuve " + this.currentAutomaton + " dans l'unité " + this.currentUnit + " en fonction du temps", x: [1, 2, 3, 4, 5],
            },
            config: {responsive: true},
          }
          break;
        case 'outsideTemperature':

          this.list.forEach(x => tempList.push(x.outsideTemperature));

          this.graph = {
            data: [
              { x: timeList, y: tempList, type: 'scatter', mode: 'lines+points', marker: {color: 'red'} },
            ],
            layout: {title: "La température a l'interrieur de la cuve " + this.currentAutomaton + " dans l'unité " + this.currentUnit + " en fonction du temps", x: [1, 2, 3, 4, 5],
            },
            config: {responsive: true},
          }
          
          break;
        case 'milkWeight':

          this.list.forEach(x => tempList.push(x.milkWeight));

          this.graph = {
            data: [
              { x: timeList, y: tempList, type: 'scatter', mode: 'lines+points', marker: {color: 'red'} },
            ],
            layout: {title: "Le poids du lait " + this.currentAutomaton + " dans l'unité " + this.currentUnit + " en fonction du temps", x: [1, 2, 3, 4, 5],
            },
            config: {responsive: true},
          }
          
          break;
        case 'finalizedProductWeight':

          this.list.forEach(x => tempList.push(x.finalizedProductWeight));

          this.graph = {
            data: [
              { x: timeList, y: tempList, type: 'scatter', mode: 'lines+points', marker: {color: 'red'} },
            ],
            layout: {title: "Le poids final en sortie " + this.currentAutomaton + " dans l'unité " + this.currentUnit + " en fonction du temps", x: [1, 2, 3, 4, 5],
            },
            config: {responsive: true},
          }
          
          break;
        case 'ph':

          this.list.forEach(x => tempList.push(x.ph));

          this.graph = {
            data: [
              { x: timeList, y: tempList, type: 'scatter', mode: 'lines+points', marker: {color: 'red'} },
            ],
            layout: {title: "La mesure du ph " + this.currentAutomaton + " dans l'unité " + this.currentUnit + " en fonction du temps", x: [1, 2, 3, 4, 5],
            },
            config: {responsive: true},
          }
          
          break;
        case 'k':

          this.list.forEach(x => tempList.push(x.k));

          this.graph = {
            data: [
              { x: timeList, y: tempList, type: 'scatter', mode: 'lines+points', marker: {color: 'red'} },
            ],
            layout: {title: "La mesure du k " + this.currentAutomaton + " dans l'unité " + this.currentUnit + " en fonction du temps", x: [1, 2, 3, 4, 5],
            },
            config: {responsive: true},
          }
          
          break;
        case 'naci':

          this.list.forEach(x => tempList.push(x.naci));

          this.graph = {
            data: [
              { x: timeList, y: tempList, type: 'scatter', mode: 'lines+points', marker: {color: 'red'} },
            ],
            layout: {title: "La mesure du naci " + this.currentAutomaton + " dans l'unité " + this.currentUnit + " en fonction du temps", x: [1, 2, 3, 4, 5],
            },
            config: {responsive: true},
          }
          
          break;
        case 'salmonel':

          this.list.forEach(x => tempList.push(x.salmonel));

          this.graph = {
            data: [
              { x: timeList, y: tempList, type: 'scatter', mode: 'lines+points', marker: {color: 'red'} },
            ],
            layout: {title: "La mesure de la salmonel " + this.currentAutomaton + " dans l'unité " + this.currentUnit + " en fonction du temps", x: [1, 2, 3, 4, 5],
            },
            config: {responsive: true},
          }
          
          break;
        case 'ecoli':

          this.list.forEach(x => tempList.push(x.ecoli));

          this.graph = {
            data: [
              { x: timeList, y: tempList, type: 'scatter', mode: 'lines+points', marker: {color: 'red'} },
            ],
            layout: {title: "La mesure de l'ecoli' " + this.currentAutomaton + " dans l'unité " + this.currentUnit + " en fonction du temps", x: [1, 2, 3, 4, 5],
            },
            config: {responsive: true},
          }
          
          break;
        case 'listeria':

          this.list.forEach(x => tempList.push(x.listeria));
          
          this.graph = {
            data: [
              { x: timeList, y: tempList, type: 'scatter', mode: 'lines+points', marker: {color: 'red'} },
            ],
            layout: {title: "La mesure de listeria " + this.currentAutomaton + " dans l'unité " + this.currentUnit + " en fonction du temps", x: [1, 2, 3, 4, 5],
            },
            config: {responsive: true},
          }
          
          break;
        default:
          this.graph = {
            data: [
                { x: ["1"], y: [1], type: 'scatter', mode: 'lines+points', marker: {color: 'red'} },
            ],
            layout: {title: 'Aucune donnéees', x: [1]},
            config: {responsive: true}
          };
          break;
      }
    }
  }
}