import {Component} from "@angular/core";
import {FormBuilder, Validators} from "@angular/forms";
import {WebService} from "../web.service";
import {ActivatedRoute, Router} from "@angular/router";
import { HttpClient } from '@angular/common/http';
import { EmailService } from '../email.service';


@Component({
  selector: 'register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})

export class RegisterComponent {
  registrationForm: any;
  public siteKey: any;
  email: any;

  constructor(public webService: WebService, private router: Router, private formBuilder: FormBuilder, private http: HttpClient, private emailService: EmailService) {
  }

  ngOnInit() {
    const navigation = this.router.getCurrentNavigation();
    const emailFromVerification = navigation && navigation.extras.state && navigation.extras.state["email"];

    this.registrationForm = this.formBuilder.group({
      first_name: ['', Validators.required],
      last_name: ['', Validators.required],
      email: [emailFromVerification || '', Validators.required],
      password: ['', Validators.required],
      postcode: ['', Validators.required],
      otp: ['', Validators.required],
      recaptcha: ['', Validators.required]
    });
    this.siteKey = "6LfJZPwjAAAAAANhjiBGN5hCBYhL4wCh4-_eFnUv"

    this.emailService.currentEmail.subscribe((email) => {
      this.registrationForm.controls['email'].setValue(email);
    });
  }

  onSubmit() {
    //console log for testing
    console.log("Data being sent:", this.registrationForm.value);
    this.webService.addVoter(this.registrationForm.value).subscribe(
      (response) => {
        console.log("Success:", response); // Add this line to log the successful response
      this.router.navigateByUrl('/login');
    },
      (error) => {
        console.error('onSubmitError:', error);
      }
    );
  }
}
