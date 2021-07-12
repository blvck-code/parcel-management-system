import { Component, OnInit } from '@angular/core';
import {ParcelsService} from "../../../services/parcels.service";
import {IParcel} from "../../../models/parcel.model";

@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.css']
})
export class AdminComponent implements OnInit {
  public 'parcels': any = []
  public totalCost: any = [];
  public 'totalRev': number | null


  constructor(
    private _parcelService: ParcelsService
  ) { }

  ngOnInit(): void {
    this._parcelService.getParcels('sent').subscribe((res: IParcel[]) => {
      this.parcels = res;
      this.handleTotalCosts()
    })
  }

  handleTotalCosts(){
    this.parcels.map((parcel: IParcel) => {
      this.totalCost = [...this.totalCost, parcel.cost]
    })
  }

  getRevenue(){

    const revenue = this.totalCost.reduce((accumulator: number, currentValue: number) => {
      return accumulator + currentValue
      }
    , 0)

    this.totalRev = revenue
  }

}
