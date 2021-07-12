import {Component, OnDestroy, OnInit} from '@angular/core';
import {ActivatedRoute, Params} from "@angular/router";
import {ParcelsService} from "../../../services/parcels.service";
import {IParcel} from "../../../models/parcel.model";
import {Subscription} from "rxjs";
import {FormBuilder, Validators} from "@angular/forms";

@Component({
  selector: 'app-parcel-detail',
  templateUrl: './parcel-detail.component.html',
  styleUrls: ['./parcel-detail.component.css']
})
export class ParcelDetailComponent implements OnInit, OnDestroy {
  public 'parcelId': number;
  public 'parcel': IParcel;
  private '_parcelSub': Subscription

  constructor(
    private _route: ActivatedRoute,
    private _parcelService: ParcelsService,
    private _fb: FormBuilder
  ) {
    _route.queryParamMap.subscribe((params: Params) => {
      if(params.get('id')){
        this.parcelId = +params.get('id')
      }
    })
  }

  ngOnInit(): void {
    this._parcelSub = this._parcelService.getParcelById(this.parcelId).subscribe((res:IParcel) => {
      this.parcel = res
      console.log(res)
    },
      error => {
      console.log(error)
      })
  }

  closeDispatchForm = this._fb.group({
    delivered: [false],
    delivered_date: ['', Validators.required]
  })

  ngOnDestroy() {
    if(this._parcelSub){
      this._parcelSub.unsubscribe()
    }
  }

  onSubmit(){
    this._parcelService.closeDispatch(this.parcelId, this.closeDispatchForm.value).subscribe((res: IParcel) => {
      this.parcel = res
      console.log(res)
    })
  }

}
