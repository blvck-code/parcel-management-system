import {Component, OnInit} from '@angular/core';
import {FormBuilder, Validators} from "@angular/forms";
import {AuthService} from "../../services/auth.service";
import {Router} from "@angular/router";
import {IUser} from "../../models/auth.model";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  public message: string = '';
  public messageStatus: any;

  constructor(
    private _fb: FormBuilder,
    private _authService: AuthService,
    private _router: Router
  ) {
  }

  ngOnInit(): void {
  }

  loginForm = this._fb.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required]]
  })

  get getEmail(){
    return this.loginForm.get('email')
  }

  get getPass(){
    return this.loginForm.get('password')
  }

  onSubmit(){
    this._authService.loginUser(this.loginForm.value).subscribe(
      res => {

        localStorage.setItem('token', res.auth_token);
        this._authService.pUserData();
        this._authService.getCurrentUser().subscribe((res:IUser) => {
          this._authService.currentUser = res
        })

        this._router.navigate(['/parcel'])
      },
      err => {
        this.messageStatus = 400;
        this.message = err;

        setTimeout(() => {
          this.messageStatus = null;
          this.message = '';
        }, 3000)
      }
    )
  }

}
