import { Injectable } from '@angular/core';
import { environment as env } from "../../environments/environment";
import {ITeller} from "../models/tellers.model";
import {Observable} from "rxjs";
import {HttpClient} from "@angular/common/http";
import {AuthService} from "./auth.service";

@Injectable({
  providedIn: 'root'
})
export class UsersService {
  private _url: string = `${env.baseURL}/users`

  constructor(
    private _http: HttpClient,
    private _authService: AuthService
  ) { }

  createUser(data: ITeller):Observable<ITeller>{
    return this._http.post<ITeller>(`${this._url}/create`, data, this._authService.getHeaders())
  }

}
