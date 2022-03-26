import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { unit } from '../object/unit';
import { ConfigService } from './config.service';
import { Observable } from 'rxjs';

@Injectable()
export class ProductionService {
  constructor(private http: HttpClient, private configService: ConfigService) { }

  getConfig() {
    return new Observable((observer) => {
      this.configService.getApiEndPoint().subscribe(x => {
        this.http.get<unit[]>(x + 'allunit').subscribe(x => observer.next(x));
      });
    });
  }

  getRequestAutomate(inutId : number) {
    return new Observable((observer) => {
      this.configService.getApiEndPoint().subscribe(x => {
        this.http.get<unit[]>(x + 'unit/' + inutId).subscribe(x => observer.next(x));
      });
    });
  }

  getRequest(inutId : number, automateId : number) {
    return new Observable((observer) => {
      this.configService.getApiEndPoint().subscribe(x => {
        this.http.get<unit[]>(x + 'productions/' + inutId + '/' + automateId).subscribe(x => observer.next(x));
      });
    });
  }
}