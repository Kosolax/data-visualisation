import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { production } from '../object/production';
import { unit } from '../object/unit';
import { automaton } from '../object/automaton';

@Injectable()
export class ProductionService {
  constructor(private http: HttpClient) { }
  
  url = 'http://localhost:8080/';

  getConfig() {
    return this.http.get<unit[]>(this.url + 'allunit');
  }

  getRequestAutomate(inutId : number) {
    return this.http.get<automaton[]>(this.url + 'unit/' + inutId);
  }

  getRequest(inutId : number, automateId : number) {
    return this.http.get<production[]>(this.url + 'productions/' + inutId + '/' + automateId);
  }
}