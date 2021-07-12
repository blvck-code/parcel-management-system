import {Component, OnInit} from '@angular/core';
import {FormBuilder, Validators} from "@angular/forms";
import {ParcelsService} from "../../../services/parcels.service";
import {IParcel, ISender} from "../../../models/parcel.model";

@Component({
  selector: 'app-parcel-add',
  templateUrl: './parcel-add.component.html',
  styleUrls: ['./parcel-add.component.css']
})
export class ParcelAddComponent implements OnInit {
  public addSenderMode: boolean = true;
  public addReceiverMode: boolean = false;
  public addParcelMode: boolean = false;
  public message: string = '';
  public 'messageStatus': number | null

  constructor(
    private _fb: FormBuilder,
    private _parcelService: ParcelsService
  ) {
  }

  ngOnInit(): void {
  }

  senderForm = this._fb.group({
    full_name: ['', [Validators.required]],
    phone: ['', [Validators.required]],
    email: ['', [Validators.required, Validators.email]],
    center: ['', [Validators.required]],
  })

  receiverForm = this._fb.group({
    full_name: ['', [Validators.required]],
    phone: ['', [Validators.required]],
    email: ['', [Validators.required, Validators.email]],
    center: ['', [Validators.required]],
  })

  parcelForm = this._fb.group({
    item: ['', [Validators.required]],
    dispatch_date: ['', [Validators.required]],
    arrival_date: ['', [Validators.required]],
    cost: ['', [Validators.required]],
    quantity: ['', [Validators.required]],
    note: ['']
  })

  proceedToSenderForm() {
    this.addSenderMode = true;
    this.addReceiverMode = false;
    this.addParcelMode = false;
  }

  proceedToReceiverForm() {
    this.addSenderMode = false;
    this.addReceiverMode = true;
    this.addParcelMode = false;
  }

  proceedToParcelForm() {
    this.addSenderMode = false;
    this.addReceiverMode = false;
    this.addParcelMode = true;
  }

  onSubmitCustomer() {
    this._parcelService.createSender(this.senderForm.value).subscribe(
      res => {
        this.proceedToReceiverForm();
        localStorage.setItem('customer_id', res.customer_id)
        this.onSuccess(res);
      },
      error => {
        this.onError(error);
      })
  }

  onSubmitReceiver(){
     this._parcelService.createReceiver(this.receiverForm.value).subscribe(
      res => {
        this.proceedToParcelForm();
        localStorage.setItem('receiver_id', res.receiver_id);
        this.onSuccess(res);
        this._parcelService.getIds();
      },
      error => {
        this.onError(error);
      })
  }

  onSubmitParcel(){
    this._parcelService.createParcel(this.parcelForm.value).subscribe(
      res => {
        this.onSuccess(res);
        this.handleSubmitSuccess();
      },
      error => {
        this.onError(error);
      })
  }

  handleSubmitSuccess(){
    this.senderForm.reset();
    this.receiverForm.reset();
    this.parcelForm.reset();
    this.proceedToSenderForm();
    localStorage.removeItem('customer_id');
    localStorage.removeItem('receiver_id');
  }

  onSuccess(res: any) {
    this.message = res.message;
    this.messageStatus = 200;

    setTimeout(() => {
      this.message = '';
      this.messageStatus = null;
    }, 3000)
  }

  onError(error: any) {
    this.message = error;
    this.messageStatus = 400;

    setTimeout(() => {
      this.message = '';
      this.messageStatus = null;
    }, 3000)
  }
}
