import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../object/environment';
import { Observable } from 'rxjs';

@Injectable()
export class ConfigService {
  constructor(private http: HttpClient) { }
    getApiEndPoint() {
        return new Observable((observer) => {
            this.http.get('assets/config.env', {responseType: 'text'}).subscribe(data => {
                data.split("\r\n").forEach(x => {
                    if (x.includes("API_EXTERNAL_PORT")) {
                        environment.api_port = +x.split("=")[1].split("\"")[1]
                    }
                })
    
                observer.next("http://localhost:" + environment.api_port + "/");
            });
          });
    }
}