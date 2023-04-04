import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import {FormBuilder, Validators} from "@angular/forms";

@Component({
  selector: 'verification',
  templateUrl: 'verification.component.html',
})
export class VerificationComponent {
  email: any;
  verificationForm: any;

  constructor(private http: HttpClient, private router: Router, private formBuilder: FormBuilder) {}

  ngOnInit(){
    this.verificationForm = this.formBuilder.group({
      email: ['', Validators.required],
  });




  }
  sendOtp() {
     console.log('Sending OTP request with data:', { email: this.email });
    this.http.post('http://localhost:5000/api/v1.0/verification', { email: this.email }).subscribe(
      () => {
        // Navigate to the registration form component after sending the OTP
        this.router.navigate(['/register']);
      },
      (error) => {
        console.error('Error sending OTP:', error);
      }
    );
  }
}
