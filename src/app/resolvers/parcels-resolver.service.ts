import { Injectable } from '@angular/core';
import {ActivatedRouteSnapshot, Resolve, RouterStateSnapshot} from "@angular/router";
import {IParcel} from "../models/parcel.model";
import {Observable} from "rxjs";
import {ParcelsService} from "../services/parcels.service";

@Injectable({
  providedIn: 'root'
})
export class ParcelsResolverService implements Resolve<IParcel[]>{

  constructor(
    private _parcelService: ParcelsService
  ) { }

  resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<IParcel[]> | Promise<IParcel[]> | IParcel[] {
    return this._parcelService.getParcels('sent')
  }
}
