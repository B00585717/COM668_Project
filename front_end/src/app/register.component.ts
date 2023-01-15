import {Component} from "@angular/core";
import {FormBuilder, Validators} from "@angular/forms";
import {WebService} from "./web.service";
import {ActivatedRoute} from "@angular/router";


@Component({
  selector: 'register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})

export class RegisterComponent {
  registrationForm: any;
  public siteKey: any;
  constructor(public webService: WebService, private route: ActivatedRoute, private formBuilder: FormBuilder) {}

  title = 'recaptcha';
  ngOnInit() {

    this.registrationForm = this.formBuilder.group({
      first_name: '',
      last_name: '',
      email: '',
      password: '',
      recaptcha: ['', Validators.required]
    });
    this.siteKey = "6LfJZPwjAAAAAANhjiBGN5hCBYhL4wCh4-_eFnUv"

  }

      onSubmit() {
    console.log(this.registrationForm.value);
      this.webService.addVoter(this.registrationForm.value).subscribe((response: any) => {
        this.registrationForm.reset();
    });
  }
}
