import {Component} from "@angular/core";
import {WebService} from "../services/web.service";
import {ActivatedRoute} from "@angular/router";
import {FormBuilder} from "@angular/forms";

@Component({
  selector: 'party',
  templateUrl: './party.component.html',
  styleUrls: ['./party.component.css']
})

export class PartyComponent {

  party_list: any = [];
  party_form: any;

   constructor(public webService: WebService, private route: ActivatedRoute, private formBuilder: FormBuilder) {
  }

  ngOnInit() {
     this.party_list = this.webService.getParty(this.route.snapshot.params['id']);
  }

  onSubmit() {
    this.webService.updateParty(this.party_form.value).subscribe((response: any) => {
      this.party_form.reset();
    });

    this.party_form = this.formBuilder.group({
      party_name: '',
      image: '',
      manifestio: ''
    });


  }

}
