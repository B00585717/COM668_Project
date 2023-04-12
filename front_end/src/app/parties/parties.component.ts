import {Component} from "@angular/core";
import {WebService} from "../services/web.service";
import {ActivatedRoute} from "@angular/router";
import {FormBuilder} from "@angular/forms";

@Component({
  selector: 'parties',
  templateUrl: './parties.component.html',
  styleUrls: ['./parties.component.css']
})

export class PartiesComponent {

  party_list: any = [];
  party: any;

  constructor(public webService: WebService) {
  }

  ngOnInit() {
    this.party_list = this.webService.getParties();
    this.party = this.webService.getParty(this.party_list.partyId)
  }
}
