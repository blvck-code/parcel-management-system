import {Component, OnDestroy, OnInit} from '@angular/core';
import {ParcelsService} from "../../../services/parcels.service";
import {IParcel} from "../../../models/parcel.model";
import {Subscription} from "rxjs";
import {ActivatedRoute, Router} from "@angular/router";

@Component({
  selector: 'app-parcels',
  templateUrl: './parcels.component.html',
  styleUrls: ['./parcels.component.css']
})
export class ParcelsComponent implements OnInit, OnDestroy {
  public category: string = 'sent';
  public parcels: IParcel[] = [];
  private '_parcelSub': Subscription;

  constructor(
    private _parcelService: ParcelsService,
    private _router: Router,
    private _route: ActivatedRoute
  ) { }

  handleCategory(e: any){
    this.category = e.target.value;
    this._parcelSub = this._parcelService.getParcels(this.category).subscribe((res:IParcel[]) => {
      console.log(res)
      this.parcels = res
    })
  }

  ngOnInit(): void {
    this._parcelSub = this._parcelService.getParcels(this.category).subscribe((res:IParcel[])=> {
        this.parcels = res;
        console.log(res)
      },
      error => {
        // @todo show error
        console.log(error)
      }
    )
  }

   navigateParcelDetail(parcel: IParcel){
    this._router.navigate(['/backend/parcels', parcel.id], {
      queryParams: {
        id:parcel.id,
        delivered: parcel.delivered
      }
    })
  }

  ngOnDestroy() {
    if(this._parcelSub) {
      this._parcelSub.unsubscribe()
    }
  }

}
