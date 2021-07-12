import { Injectable } from '@angular/core';
import {Observable} from "rxjs";
import { environment as env } from "../../environments/environment";
import {IAuth} from "../models/auth.model";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Router} from "@angular/router";
import { IUser } from "../models/auth.model";

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  public 'currentUser': IUser;

  private _url: string = `${env.baseURL}/auth`

  constructor(
    private _http: HttpClient,
    private _router: Router
  ) { }

  handleAdmin() {
    this.logOut();
    this._router.navigate(['/backend/login']);
  }

  pUserData(){
    this.getCurrentUser().subscribe((res:IUser) => {
      console.log(res)
      this.currentUser = res;
    })
  }

  getToken() {
    return localStorage.getItem('token');
  }

  getHeaders() {
    let headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${this.getToken()}`
    });

    return { headers };
  }

  logOut(){
    localStorage.removeItem('token');
    this._router.navigate(['/'])
  }

  loggedIn() {
    return !!localStorage.getItem('token');
  }

  loginUser(data: IAuth):Observable<any>{
    return this._http.post<any>(`${this._url}/login`, data)
  }

  getCurrentUser():Observable<IUser>{
    return this._http.get<IUser>(`${this._url}/user`, this.getHeaders())
  }


}
