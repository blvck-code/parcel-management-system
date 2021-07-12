import { Injectable } from '@angular/core';
import {Observable} from "rxjs";
import { environment as env } from "../../environments/environment";
import {HttpClient} from "@angular/common/http";
import {ITeller} from '../models/tellers.model'
import {AuthService} from "./auth.service";

@Injectable({
  providedIn: 'root'
})
export class TellersService {
  private _url: string = `${env.baseURL}/users`

  constructor(
    private _http: HttpClient,
    private _authService: AuthService
  ) { }

  getTellers():Observable<ITeller[]>{
    return this._http.get<ITeller[]>(`${this._url}/list`, this._authService.getHeaders())
  }
}
