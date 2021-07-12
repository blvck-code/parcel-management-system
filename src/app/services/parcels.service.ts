import { Injectable } from '@angular/core';
import {Observable} from "rxjs";
import {IParcel, IReceiver, ISender} from "../models/parcel.model";
import {environment as env} from "../../environments/environment";
import {HttpClient, HttpHeaders, HttpParams} from "@angular/common/http";
import {AuthService} from "./auth.service";

@Injectable({
  providedIn: 'root'
})
export class ParcelsService {
  private _url: string = `${env.baseURL}`

  public customerId: any = '';
  public receiverId: any = '';

  constructor(
    private _http: HttpClient,
    private _authService: AuthService
  ) { }

  createSender(data: ISender): Observable<any>{
    return this._http.post<any>(`${this._url}/customer/create`, data, this._authService.getHeaders())
  }

  createReceiver(data: IReceiver): Observable<any>{
    return this._http.post<any>(`${this._url}/receiver/create`, data, this._authService.getHeaders())
  }

  getIds(){
    this.customerId = localStorage.getItem('customer_id');
    this.receiverId = localStorage.getItem('receiver_id');
  }

 createParcel(data: any): Observable<any>{
    let headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${this._authService.getToken()}`
    })

   let params = new HttpParams().set('customer_id',this.customerId).set('receiver_id', this.receiverId)

   let parcel = JSON.stringify({
     'parcel': data,
     'customer_id': this.customerId,
     'receiver_id': this.receiverId
   })
    return this._http.post<any>(`${this._url}/parcels/create`, parcel, this._authService.getHeaders())
  }

  getParcels(category: string):Observable<IParcel[]>{
    let headers = new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this._authService.getToken()}`
      })

    let params = new HttpParams().set('category', category);

    return this._http.get<IParcel[]>(`${this._url}/parcels/list`, {
      headers: headers,
      params: params
    })
  }

  getParcelById(id: number):Observable<IParcel>{
    return this._http.get<IParcel>(`${this._url}/parcels/${id}`)
  }

  closeDispatch(id: number, data: any):Observable<any>{
    return this._http.put<any>(`${this._url}/parcels/${id}`, data, this._authService.getHeaders())
  }

}
