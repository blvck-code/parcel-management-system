import {Injectable, Injector} from '@angular/core';
import {HttpEvent, HttpHandler, HttpInterceptor, HttpRequest} from "@angular/common/http";
import {Observable} from "rxjs";
import {AuthService} from "../services/auth.service";

@Injectable({
  providedIn: 'root'
})
export class TokenInterceptorService implements HttpInterceptor{

  constructor(private injector: Injector) { }

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    let _authService = this.injector.get(AuthService);
    let tokenReq = req.clone({
      setHeaders: {
        Authorization: `Bearer ${_authService.getToken()}`
      }
    })
    return next.handle(tokenReq)
  }
}
