import { Injectable } from '@angular/core';
import {
  HttpErrorResponse,
  HttpEvent,
  HttpHandler,
  HttpInterceptor,
  HttpRequest,
} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';
import { Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Injectable({
  providedIn: 'root',
})
export class ErrorHandlerInterceptorService implements HttpInterceptor {
  constructor(private _router: Router, private _authService: AuthService) {}

  intercept(
    req: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    return next.handle(req).pipe(
      retry(1),
      catchError((err: HttpErrorResponse) => {
        let errorMsg = '';

        if (err.error instanceof ErrorEvent) {
          // client-side Error
          errorMsg = `Error: ${err.error.message}`;
        } else {
          // server-side Erro
          errorMsg = `Error: ${err.error.message}`;
          if (err.status === 401 || err.status === 402) {
            this._authService.logOut();
            this._router.navigate(['/']);
          } else if (err.status === 500) {
            this._router.navigate(['/server-error']);
          }

        }

        return throwError(errorMsg);
      })
    );
  }
}
