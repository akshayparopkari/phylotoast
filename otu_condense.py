'''
Created on Nov 27, 2012

@author: Shareef M Dabdoub
@author Matthew Mason
'''
import argparse

#TODO: allow for tree level selection (i.e. stop at genus level)
def prune_taxonomy(taxF):
    """
    :@type taxF: file
    :@param taxF: The taxonomy output file to parse
    
    :@rtype: dict
    :@return: A dictionary of taxonomy strings keyed on OTU ID 
    """
    uniqueTax = {}
    nuTax = {}  #non-unique taxonomies
    
    for line in taxF:
        otuID, tax, floatVal, otuIDr = line.split()
        if not tax in uniqueTax:
            uniqueTax[tax] = otuID, floatVal, otuIDr
            nuTax[uniqueTax[tax][0]] = []
        else:
            nuTax[uniqueTax[tax][0]].append(otuID)
    
    ut = {otuID: (tax, floatVal, otuIDr) for tax,(otuID, floatVal, otuIDr) in 
          uniqueTax.iteritems()}
    
    return ut, nuTax
    

def handle_program_options():
    parser = argparse.ArgumentParser(description="Take a taxonomy table \
                                     from the assign_taxonomy QIIME script \
                                     and prune all redundant taxonomy strings")
    parser.add_argument('input_taxonomy', help="The taxonomy file output by \
                                                the assign_taxonomy script.")
    parser.add_argument('-p', '--pruned_output_file', 
                        default='condensed_rep_set_tax_assignments.txt',
                        help="The output file for the pruned taxonomy list.")
    parser.add_argument('-n', '--non_unique_output_file', 
                        default='nonunique_otu_matrix.txt',
                        help="The file will contain a list of pruned OTU IDs \
                              associated with the OTU IDs they replaced.")
    parser.add_argument('-v', '--verbose', action='store_true')
    
    return parser.parse_args()
        

    
def main():
    args = handle_program_options()
    
    with open(args.input_taxonomy, 'rU') as taxF:
        uniqueTaxonomies, nonuniqueTaxonomies = prune_taxonomy(taxF)
    
    with open(args.pruned_output_file, 'w') as poF:
        for otuID, (tax, floatVal, otuIDr) in uniqueTaxonomies.iteritems():
            poF.write("%s\t%s\t%s\t%s\n" % (otuID, tax, floatVal, otuIDr))
    
    with open(args.non_unique_output_file, 'w') as nuoF:
        nuID_count = 0
        for key in nonuniqueTaxonomies:
            nuoF.write('%s\t%s\n' % (key,'\t'.join(nonuniqueTaxonomies[key])))
            if len(nonuniqueTaxonomies[key]) > 0:
                nuID_count += len(nonuniqueTaxonomies[key])

    if args.verbose:
        print '%i unique OTUs discovered' % len(uniqueTaxonomies)
        print '%i non-unique OTU records eliminated' % nuID_count



















if __name__ == '__main__':
    main()