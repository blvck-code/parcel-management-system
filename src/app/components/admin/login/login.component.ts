import {Component, OnInit} from '@angular/core';
import {FormBuilder, Validators} from "@angular/forms";
import {AuthService} from "../../../services/auth.service";
import {Router} from "@angular/router";
import {IUser} from "../../../models/auth.model";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})

export class LoginComponent implements OnInit {
  public message: string = '';
  public messageStatus: any;

  constructor(
    private _fb: FormBuilder,
    private _authService: AuthService,
    private _router: Router,
  ) {
  }

  ngOnInit(): void {

  }

  get getEmail() {
    return this.loginForm.get('email')
  }

  get getPass() {
    return this.loginForm.get('password')
  }

  loginForm = this._fb.group({
    email: ['', [Validators.required, Validators.email]],
    password: ['', [Validators.required]]
  })

  onSubmit() {
    this._authService.loginUser(this.loginForm.value).subscribe(
      res => {
        if (res.role === 'admin') {
          localStorage.setItem('token', res.auth_token);
          this._authService.pUserData();
          this._authService.getCurrentUser().subscribe((res: IUser) => {
            this._authService.currentUser = res
          })

          this._router.navigate(['/backend'])
        } else {
          this.messageStatus = 400;
          this.message = 'You are not authorised to access this page'
          this._authService.handleAdmin()

          setTimeout(() => {
            this.messageStatus = null;
            this.message = '';
          }, 3000)
        }

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
