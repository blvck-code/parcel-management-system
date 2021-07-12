import {Component, OnDestroy, OnInit} from '@angular/core';
import {TellersService} from "../../../../services/tellers.service";
import {Subscription} from "rxjs";
import {ITeller} from "../../../../models/tellers.model";
import {FormBuilder, Validators} from "@angular/forms";
import {UsersService} from "../../../../services/users.service";

@Component({
  selector: 'app-tellers',
  templateUrl: './tellers.component.html',
  styleUrls: ['./tellers.component.css']
})
export class TellersComponent implements OnInit, OnDestroy {
  private '_tellerSub': Subscription;
  public 'tellers': ITeller[];
  public addMode: boolean = false;
  public message: string = '';
  public 'messageStatus': number | null;

  constructor(
    private _tellerService: TellersService,
    private _fb: FormBuilder,
    private _userService: UsersService
  ) {
  }

  ngOnInit(): void {
    this._tellerSub = this._tellerService.getTellers().subscribe((res: ITeller[]) => {
      this.tellers = res;
      console.log(this.tellers)
    })
  }

  addTellerForm = this._fb.group({
    first_name: ['', [Validators.required]],
    last_name: ['', [Validators.required]],
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required]],
  })

  toggleAddMode() {
    this.addMode = !this.addMode
  }

  onSubmit() {
    this._userService.createUser(this.addTellerForm.value).subscribe(
      res => {
        this.tellers = [res, ...this.tellers];
        this.onSuccess();
        this.addTellerForm.reset()
      },
      err => {
        this.onError(err)
      }
    )
  }

  onSuccess(){
    this.message = 'User added successfully';
    this.messageStatus = 200;

    setTimeout(() => {
      this.messageStatus = null;
      this.message = '';
    }, 3000)
  }

  onError(err: string) {
    this.message = err;
    this.messageStatus = 400;

    setTimeout(() => {
      this.messageStatus = null;
      this.message = '';
    }, 3000)
  }


  ngOnDestroy() {
    if (this._tellerSub) {
      this._tellerSub.unsubscribe();
    }
  }
}
